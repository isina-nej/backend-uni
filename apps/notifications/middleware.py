# ==============================================================================
# WEBSOCKET MIDDLEWARE FOR DJANGO CHANNELS
# میان‌افزار وب‌سوکت برای جنگو چنلز
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from urllib.parse import parse_qs
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """JWT Authentication middleware for WebSocket connections"""
    
    def __init__(self, inner):
        super().__init__(inner)
    
    async def __call__(self, scope, receive, send):
        # Only process WebSocket connections
        if scope['type'] != 'websocket':
            return await super().__call__(scope, receive, send)
        
        # Try to authenticate user
        user = await self.authenticate_user(scope)
        scope['user'] = user
        
        return await super().__call__(scope, receive, send)
    
    async def authenticate_user(self, scope):
        """Authenticate user from WebSocket connection"""
        try:
            # Get query parameters
            query_params = parse_qs(scope.get('query_string', b'').decode())
            
            # Look for token in query parameters
            token = None
            if 'token' in query_params:
                token = query_params['token'][0]
            
            # Look for token in headers (Authorization header)
            if not token:
                headers = dict(scope.get('headers', []))
                auth_header = headers.get(b'authorization', b'').decode()
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
            
            # Look for token in subprotocols (alternative method)
            if not token:
                subprotocols = scope.get('subprotocols', [])
                for protocol in subprotocols:
                    if protocol.startswith('token.'):
                        token = protocol.split('.', 1)[1]
                        break
            
            if not token:
                logger.warning("No authentication token found in WebSocket connection")
                return AnonymousUser()
            
            # Validate JWT token
            try:
                UntypedToken(token)
                user = await self.get_user_from_token(token)
                if user:
                    logger.info(f"WebSocket authenticated for user: {user.username}")
                    return user
                else:
                    logger.warning("Invalid user from token")
                    return AnonymousUser()
            
            except (InvalidToken, TokenError) as e:
                logger.warning(f"Invalid JWT token in WebSocket: {e}")
                return AnonymousUser()
        
        except Exception as e:
            logger.error(f"Error authenticating WebSocket user: {e}")
            return AnonymousUser()
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        """Get user from JWT token"""
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            
            # Decode token to get user ID
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            
            # Get user from database
            user = User.objects.get(id=user_id, is_active=True)
            return user
        
        except (User.DoesNotExist, InvalidToken, TokenError, KeyError) as e:
            logger.warning(f"Error getting user from token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error getting user from token: {e}")
            return None


class WebSocketLoggingMiddleware(BaseMiddleware):
    """Middleware for logging WebSocket connections"""
    
    def __init__(self, inner):
        super().__init__(inner)
    
    async def __call__(self, scope, receive, send):
        # Only process WebSocket connections
        if scope['type'] != 'websocket':
            return await super().__call__(scope, receive, send)
        
        # Log connection attempt
        client_info = self.get_client_info(scope)
        logger.info(f"WebSocket connection attempt from {client_info}")
        
        return await super().__call__(scope, receive, send)
    
    def get_client_info(self, scope):
        """Extract client information from scope"""
        try:
            client = scope.get('client', ['unknown', 0])
            headers = dict(scope.get('headers', []))
            user_agent = headers.get(b'user-agent', b'Unknown').decode('utf-8')
            
            return f"{client[0]}:{client[1]} - {user_agent[:100]}"
        except Exception:
            return "unknown client"


class WebSocketRateLimitMiddleware(BaseMiddleware):
    """Basic rate limiting for WebSocket connections"""
    
    def __init__(self, inner):
        super().__init__(inner)
        self.connection_count = {}
        self.max_connections_per_ip = 10
    
    async def __call__(self, scope, receive, send):
        # Only process WebSocket connections
        if scope['type'] != 'websocket':
            return await super().__call__(scope, receive, send)
        
        # Check rate limit
        client_ip = scope.get('client', ['unknown'])[0]
        
        if self.is_rate_limited(client_ip):
            logger.warning(f"Rate limit exceeded for IP {client_ip}")
            # Close connection immediately
            await send({
                'type': 'websocket.close',
                'code': 4008  # Policy violation
            })
            return
        
        # Track connection
        self.track_connection(client_ip, True)
        
        try:
            return await super().__call__(scope, receive, send)
        finally:
            # Remove connection tracking
            self.track_connection(client_ip, False)
    
    def is_rate_limited(self, client_ip):
        """Check if client IP is rate limited"""
        current_count = self.connection_count.get(client_ip, 0)
        return current_count >= self.max_connections_per_ip
    
    def track_connection(self, client_ip, is_connecting):
        """Track connection count for IP"""
        if is_connecting:
            self.connection_count[client_ip] = self.connection_count.get(client_ip, 0) + 1
        else:
            current_count = self.connection_count.get(client_ip, 0)
            if current_count > 0:
                self.connection_count[client_ip] = current_count - 1
            if self.connection_count.get(client_ip, 0) == 0:
                self.connection_count.pop(client_ip, None)


class WebSocketPermissionMiddleware(BaseMiddleware):
    """Permission checking middleware for WebSocket connections"""
    
    def __init__(self, inner):
        super().__init__(inner)
    
    async def __call__(self, scope, receive, send):
        # Only process WebSocket connections
        if scope['type'] != 'websocket':
            return await super().__call__(scope, receive, send)
        
        # Check permissions based on URL path
        path = scope.get('path', '')
        user = scope.get('user')
        
        if not self.has_permission(path, user):
            logger.warning(f"Permission denied for WebSocket path {path} for user {getattr(user, 'username', 'anonymous')}")
            # Close connection with permission denied
            await send({
                'type': 'websocket.close',
                'code': 4003  # Forbidden
            })
            return
        
        return await super().__call__(scope, receive, send)
    
    def has_permission(self, path, user):
        """Check if user has permission to access WebSocket path"""
        # Admin paths require staff permission
        if '/admin/' in path:
            return user and user.is_authenticated and user.is_staff
        
        # Regular notification paths require authentication
        if '/notifications/' in path:
            return user and user.is_authenticated
        
        # Broadcast paths allow authenticated users
        if '/broadcasts/' in path:
            return user and user.is_authenticated
        
        # Allow other paths by default
        return True


# Middleware stack composition
def JWTAuthMiddlewareStack(inner):
    """Complete middleware stack for WebSocket authentication"""
    return JWTAuthMiddleware(
        WebSocketLoggingMiddleware(
            WebSocketRateLimitMiddleware(
                WebSocketPermissionMiddleware(inner)
            )
        )
    )
