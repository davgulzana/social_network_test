from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Post

from post import utils as likes_services

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", read_only=True)
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("text", "image", "created_at", "uuid", "is_fan", "total_likes")

    def get_is_fan(self, obj) -> bool:
        """
        Checks whether 'request.user' liked the post ('obj').
        """
        user = self.context.get("request").user
        return likes_services.is_fan(obj, user)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["author_id"] = request.user.id
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["text"] = instance.text
        representation["author"] = instance.author.email
        return representation


class LikesAnalyticsSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y")
    total_likes = serializers.IntegerField()

    def to_representation(self, instance):
        representation = super(LikesAnalyticsSerializer, self).to_representation(
            instance
        )
        date = representation.pop("created_at")
        representation["date"] = date
        return representation
