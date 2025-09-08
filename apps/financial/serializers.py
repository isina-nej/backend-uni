from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'user_name', 'amount', 'description', 'payment_date', 'is_paid']
