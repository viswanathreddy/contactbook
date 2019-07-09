from rest_framework import serializers

from v1.contacts.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data_email = validated_data.get('email', instance.email)
        if instance.email != validated_data_email:
            raise serializers.ValidationError('cannot update email field')
        instance.email = validated_data_email
        instance.name = validated_data.get('name', instance.name)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.save()
        return instance
