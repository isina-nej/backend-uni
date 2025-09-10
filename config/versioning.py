# ==============================================================================
# API VERSIONING FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.versioning import AcceptHeaderVersioning, URLPathVersioning
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _


class CustomAcceptHeaderVersioning(AcceptHeaderVersioning):
    """Custom Accept Header Versioning with enhanced features"""
    
    allowed_versions = ['1.0', '1.1']
    version_param = 'version'
    default_version = '1.0'
    
    def determine_version(self, request, *args, **kwargs):
        """Determine API version from Accept header"""
        version = super().determine_version(request, *args, **kwargs)
        
        # Log version usage for analytics
        if hasattr(request, 'user') and request.user.is_authenticated:
            # You can add logging here for version analytics
            pass
            
        return version
    
    def reverse(self, viewname, args=None, kwargs=None, request=None, format=None, **extra):
        """Enhanced reverse URL with version support"""
        return super().reverse(viewname, args, kwargs, request, format, **extra)
    
    def is_allowed_version(self, version):
        """Check if version is allowed"""
        return version in self.allowed_versions


class CustomURLPathVersioning(URLPathVersioning):
    """Custom URL Path Versioning"""
    
    allowed_versions = ['v1', 'v2']
    version_param = 'version'
    default_version = 'v1'
    
    def determine_version(self, request, *args, **kwargs):
        """Determine version from URL path"""
        version = super().determine_version(request, *args, **kwargs)
        
        # Handle version-specific logic
        if version == 'v2':
            # Add any v2 specific handling
            request.api_version_features = ['enhanced_filtering', 'bulk_operations']
        else:
            request.api_version_features = ['basic_filtering']
            
        return version


class VersionedViewMixin:
    """Mixin to add version-aware functionality to views"""
    
    def get_serializer_class(self):
        """Get version-specific serializer"""
        serializer_class = super().get_serializer_class()
        
        # Check for version-specific serializers
        version = getattr(self.request, 'version', '1.0')
        version_key = version.replace('.', '_')
        
        # Look for version-specific serializer
        version_serializer_name = f"{serializer_class.__name__}V{version_key}"
        version_serializer = getattr(self, f'serializer_class_v{version_key}', None)
        
        if version_serializer:
            return version_serializer
            
        return serializer_class
    
    def get_queryset(self):
        """Get version-specific queryset"""
        queryset = super().get_queryset()
        version = getattr(self.request, 'version', '1.0')
        
        # Apply version-specific filtering or optimization
        if version == '1.1':
            # Enhanced queryset for v1.1
            if hasattr(queryset, 'select_related'):
                return queryset.select_related()
        
        return queryset
    
    def get_permissions(self):
        """Get version-specific permissions"""
        permissions = super().get_permissions()
        version = getattr(self.request, 'version', '1.0')
        
        # Apply version-specific permissions
        if version == '2.0':
            # More strict permissions for v2.0
            from rest_framework.permissions import IsAdminUser
            permissions.append(IsAdminUser())
            
        return permissions


def get_api_version_info():
    """Get comprehensive API version information"""
    return {
        'current_version': '1.0',
        'supported_versions': ['1.0', '1.1'],
        'deprecated_versions': [],
        'version_details': {
            '1.0': {
                'release_date': '2024-01-01',
                'status': 'stable',
                'features': [
                    'Basic CRUD operations',
                    'Authentication',
                    'Basic filtering',
                    'Pagination'
                ],
                'changes': 'Initial release'
            },
            '1.1': {
                'release_date': '2024-06-01',
                'status': 'stable',
                'features': [
                    'Enhanced filtering',
                    'Bulk operations',
                    'Improved caching',
                    'Better error handling'
                ],
                'changes': [
                    'Added advanced filtering options',
                    'Improved performance with caching',
                    'Enhanced error messages',
                    'Added bulk operations support'
                ]
            }
        },
        'migration_guides': {
            '1.0_to_1.1': {
                'breaking_changes': [],
                'new_features': [
                    'Advanced filtering with CourseFilter',
                    'Bulk enrollment operations',
                    'Enhanced error responses'
                ],
                'deprecations': [],
                'recommendations': [
                    'Update client to use new filtering parameters',
                    'Handle enhanced error response format',
                    'Consider using bulk operations for better performance'
                ]
            }
        }
    }


class APIVersionInfoView:
    """View to provide API version information"""
    
    def get(self, request):
        """Get API version information"""
        version_info = get_api_version_info()
        return Response(version_info)


# Version-specific serializer examples
class VersionedSerializerMixin:
    """Mixin for creating version-aware serializers"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get version from context
        request = self.context.get('request')
        if request:
            version = getattr(request, 'version', '1.0')
            self.api_version = version
            
            # Apply version-specific field modifications
            self._apply_version_specific_fields()
    
    def _apply_version_specific_fields(self):
        """Apply version-specific field modifications"""
        if hasattr(self, 'api_version'):
            if self.api_version == '1.1':
                # Add new fields for v1.1
                self._add_v11_fields()
            elif self.api_version == '2.0':
                # Modify fields for v2.0
                self._modify_v20_fields()
    
    def _add_v11_fields(self):
        """Add fields specific to version 1.1"""
        # Example: Add calculated fields
        if 'enhanced_info' not in self.fields:
            from rest_framework import serializers
            self.fields['enhanced_info'] = serializers.SerializerMethodField()
    
    def _modify_v20_fields(self):
        """Modify fields for version 2.0"""
        # Example: Remove deprecated fields
        deprecated_fields = ['old_field', 'legacy_data']
        for field in deprecated_fields:
            if field in self.fields:
                del self.fields[field]
    
    def get_enhanced_info(self, obj):
        """Get enhanced information for v1.1+"""
        if hasattr(self, 'api_version') and self.api_version >= '1.1':
            return {
                'created_timestamp': obj.created_at.timestamp() if hasattr(obj, 'created_at') else None,
                'last_modified': obj.updated_at.timestamp() if hasattr(obj, 'updated_at') else None,
            }
        return None


# Decorator for version-specific endpoints
def version_required(*versions):
    """Decorator to require specific API versions"""
    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            current_version = getattr(request, 'version', '1.0')
            if current_version not in versions:
                return Response({
                    'error': True,
                    'message': _('این endpoint در نسخه فعلی API پشتیبانی نمی‌شود'),
                    'required_versions': list(versions),
                    'current_version': current_version
                }, status=status.HTTP_400_BAD_REQUEST)
            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator


# Version compatibility checker
class VersionCompatibilityChecker:
    """Check version compatibility and provide migration guidance"""
    
    @staticmethod
    def check_compatibility(current_version, target_version):
        """Check if migration from current to target version is possible"""
        version_order = ['1.0', '1.1', '2.0']
        
        try:
            current_index = version_order.index(current_version)
            target_index = version_order.index(target_version)
            
            return {
                'compatible': True,
                'upgrade_path': version_order[current_index:target_index + 1],
                'breaking_changes': current_index < target_index,
                'recommendations': [
                    'Review API documentation for changes',
                    'Test thoroughly before upgrading',
                    'Update client libraries'
                ]
            }
        except ValueError:
            return {
                'compatible': False,
                'error': 'Unknown version specified'
            }
    
    @staticmethod
    def get_migration_steps(from_version, to_version):
        """Get detailed migration steps"""
        if from_version == '1.0' and to_version == '1.1':
            return [
                'Update filtering parameters to use new CourseFilter',
                'Handle enhanced error response format',
                'Update pagination handling',
                'Test bulk operations if using them'
            ]
        return ['Consult API documentation for migration details']
