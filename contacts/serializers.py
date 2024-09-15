from rest_framework import serializers
from .models import User, Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'name', 'phone_number', 'is_spam']
        
class DetailedUserSerializer(serializers.ModelSerializer):
    is_spam = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'is_spam']

    def get_is_spam(self, obj):
        return Contact.objects.filter(phone_number=obj.phone_number, is_spam=True).exists()

    def get_email(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.email
        return None

class DetailedContactSerializer(serializers.ModelSerializer):
    is_spam = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'is_spam']

    def get_is_spam(self, obj):
        return obj.is_spam