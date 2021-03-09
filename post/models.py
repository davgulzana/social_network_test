import uuid

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="likes", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")


class Post(models.Model):
    uuid = models.UUIDField(unique=True, blank=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="posts"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="posts", null=True)
    likes = GenericRelation(Like)

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        if not self.uuid:
            self.uuid = str(uuid.uuid4())
        super().save(*args, **kwargs)
