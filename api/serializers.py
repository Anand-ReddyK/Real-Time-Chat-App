from rest_framework import serializers

from chat import models


class SingleChatSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Room
        fields = '__all__'
