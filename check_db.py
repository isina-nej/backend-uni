#!/usr/bin/env python3
import os
import sys
import django

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_local')
django.setup()

from apps.users.models import *

print("=== DATABASE STATUS ===")
print(f"OrganizationalUnit count: {OrganizationalUnit.objects.count()}")
print(f"Position count: {Position.objects.count()}")
print(f"Permission count: {Permission.objects.count()}")
print(f"User count: {User.objects.count()}")
print(f"UserPosition count: {UserPosition.objects.count()}")
print(f"UserPermission count: {UserPermission.objects.count()}")
print(f"AccessLog count: {AccessLog.objects.count()}")

print("\n=== ORGANIZATIONAL UNITS ===")
for unit in OrganizationalUnit.objects.all()[:5]:
    print(f"- {unit.name} - Type: {unit.unit_type}")

print("\n=== USERS ===")
for user in User.objects.all()[:5]:
    print(f"- {user.username}: {user.get_full_name()} - Role: {user.role}")

print("\n=== POSITIONS ===")
for pos in Position.objects.all()[:5]:
    print(f"- {pos.title} - Level: {pos.position_level}")

print("\n=== PERMISSIONS ===")
for perm in Permission.objects.all()[:5]:
    print(f"- {perm.name} - Type: {perm.permission_type}")
