# ==============================================================================
# CUSTOM PAGINATION FOR UNIVERSITY MANAGEMENT SYSTEM
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict
import math


class CustomPagination(PageNumberPagination):
    """Advanced pagination with metadata"""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Return paginated response with enhanced metadata"""
        next_page = self.get_next_link()
        previous_page = self.get_previous_link()
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        total_items = self.page.paginator.count

        # Calculate page info
        start_index = (current_page - 1) * self.page_size + 1
        end_index = min(current_page * self.page_size, total_items)

        # Calculate progress percentage
        progress_percentage = (current_page / total_pages) * 100 if total_pages > 0 else 100

        return Response(OrderedDict([
            ('count', total_items),
            ('total_pages', total_pages),
            ('current_page', current_page),
            ('page_size', self.page_size),
            ('start_index', start_index),
            ('end_index', end_index),
            ('progress_percentage', round(progress_percentage, 2)),
            ('has_next', self.page.has_next()),
            ('has_previous', self.page.has_previous()),
            ('next', next_page),
            ('previous', previous_page),
            ('results', data)
        ]))

    def get_paginated_response_schema(self, schema):
        """Enhanced schema for pagination"""
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'description': 'Total number of items'
                },
                'total_pages': {
                    'type': 'integer',
                    'description': 'Total number of pages'
                },
                'current_page': {
                    'type': 'integer',
                    'description': 'Current page number'
                },
                'page_size': {
                    'type': 'integer',
                    'description': 'Number of items per page'
                },
                'start_index': {
                    'type': 'integer',
                    'description': 'Start index of current page'
                },
                'end_index': {
                    'type': 'integer',
                    'description': 'End index of current page'
                },
                'progress_percentage': {
                    'type': 'number',
                    'description': 'Progress percentage through results'
                },
                'has_next': {
                    'type': 'boolean',
                    'description': 'Whether there is a next page'
                },
                'has_previous': {
                    'type': 'boolean',
                    'description': 'Whether there is a previous page'
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL to next page'
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'description': 'URL to previous page'
                },
                'results': schema,
            },
        }


class LargeDatasetPagination(CustomPagination):
    """Pagination for large datasets with performance optimizations"""

    page_size = 50
    max_page_size = 200

    def paginate_queryset(self, queryset, request, view=None):
        """Optimize pagination for large datasets"""
        # Add select_related and prefetch_related if available
        if hasattr(view, 'get_queryset'):
            queryset = self.optimize_queryset(queryset, view)

        return super().paginate_queryset(queryset, request, view)

    def optimize_queryset(self, queryset, view):
        """Add database optimizations"""
        # This can be extended based on specific model relationships
        return queryset


class CursorPagination:
    """Cursor-based pagination for real-time data"""

    def __init__(self):
        self.page_size = 20
        self.ordering = '-created_at'

    def paginate_queryset(self, queryset, request, view=None):
        """Implement cursor-based pagination"""
        cursor = request.query_params.get('cursor')
        if cursor:
            # Parse cursor and filter queryset
            queryset = queryset.filter(created_at__lt=cursor)

        return queryset.order_by(self.ordering)[:self.page_size]
