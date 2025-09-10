# ==============================================================================
# WEBSOCKET ROUTING CONFIGURATION
# پیکربندی مسیریابی وب‌سوکت
# تاریخ ایجاد: ۱۴۰۳/۰۶/۲۰
# ==============================================================================

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # User notifications WebSocket
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
    
    # Global broadcasts WebSocket  
    re_path(r'ws/broadcasts/$', consumers.NotificationBroadcastConsumer.as_asgi()),
    
    # Admin monitoring WebSocket
    re_path(r'ws/admin/monitoring/$', consumers.AdminNotificationConsumer.as_asgi()),
]
