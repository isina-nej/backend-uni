from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import (
    DormitoryAccommodation, DormitoryRoom, 
    DormitoryMaintenance
)


@receiver(post_save, sender=DormitoryAccommodation)
def update_room_status(sender, instance, created, **kwargs):
    """به‌روزرسانی وضعیت اتاق هنگام تغییر اسکان"""
    room = instance.room
    
    # محاسبه تعداد ساکنان فعال
    active_accommodations = DormitoryAccommodation.objects.filter(
        room=room,
        status__in=['APPROVED', 'ACTIVE'],
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()
    ).count()
    
    # به‌روزرسانی وضعیت اتاق
    if active_accommodations == 0:
        room.status = 'AVAILABLE'
    elif active_accommodations >= room.capacity:
        room.status = 'OCCUPIED'
    else:
        room.status = 'AVAILABLE'  # جای خالی دارد
    
    room.save(update_fields=['status'])


@receiver(pre_save, sender=DormitoryAccommodation)
def set_accommodation_approval_time(sender, instance, **kwargs):
    """تنظیم زمان تأیید هنگام تغییر وضعیت به تأیید شده"""
    if instance.pk:
        try:
            old_instance = DormitoryAccommodation.objects.get(pk=instance.pk)
            if (old_instance.status != 'APPROVED' and 
                instance.status == 'APPROVED' and 
                not instance.approved_at):
                instance.approved_at = timezone.now()
        except DormitoryAccommodation.DoesNotExist:
            pass
    elif instance.status == 'APPROVED' and not instance.approved_at:
        instance.approved_at = timezone.now()


@receiver(pre_save, sender=DormitoryMaintenance)
def set_maintenance_timestamps(sender, instance, **kwargs):
    """تنظیم زمان‌های مختلف بر اساس تغییر وضعیت"""
    if instance.pk:
        try:
            old_instance = DormitoryMaintenance.objects.get(pk=instance.pk)
            
            # تنظیم زمان محولی
            if (old_instance.status != 'ASSIGNED' and 
                instance.status == 'ASSIGNED' and 
                not instance.assigned_at):
                instance.assigned_at = timezone.now()
            
            # تنظیم زمان شروع
            if (old_instance.status != 'IN_PROGRESS' and 
                instance.status == 'IN_PROGRESS' and 
                not instance.started_at):
                instance.started_at = timezone.now()
            
            # تنظیم زمان تکمیل
            if (old_instance.status != 'COMPLETED' and 
                instance.status == 'COMPLETED' and 
                not instance.completed_at):
                instance.completed_at = timezone.now()
                
        except DormitoryMaintenance.DoesNotExist:
            pass


@receiver(post_save, sender=DormitoryMaintenance)
def update_room_maintenance_status(sender, instance, created, **kwargs):
    """به‌روزرسانی وضعیت نگهداری اتاق"""
    room = instance.room
    
    # بررسی درخواست‌های تعمیر فعال
    active_maintenance = DormitoryMaintenance.objects.filter(
        room=room,
        status__in=['REPORTED', 'ASSIGNED', 'IN_PROGRESS']
    ).exists()
    
    # اگر درخواست تعمیر فعال دارد و اولویت بالا دارد
    urgent_maintenance = DormitoryMaintenance.objects.filter(
        room=room,
        status__in=['REPORTED', 'ASSIGNED', 'IN_PROGRESS'],
        priority__in=['HIGH', 'URGENT']
    ).exists()
    
    # به‌روزرسانی وضعیت اتاق
    if urgent_maintenance:
        if room.status != 'OUT_OF_ORDER':
            room.status = 'OUT_OF_ORDER'
            room.save(update_fields=['status'])
    elif active_maintenance:
        if room.status != 'MAINTENANCE':
            room.status = 'MAINTENANCE'
            room.save(update_fields=['status'])
    elif not active_maintenance and room.status in ['MAINTENANCE', 'OUT_OF_ORDER']:
        # بررسی تعداد ساکنان فعلی برای تنظیم وضعیت مناسب
        current_occupancy = room.current_occupancy
        if current_occupancy == 0:
            room.status = 'AVAILABLE'
        elif current_occupancy >= room.capacity:
            room.status = 'OCCUPIED'
        else:
            room.status = 'AVAILABLE'
        room.save(update_fields=['status'])
