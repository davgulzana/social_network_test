from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like

User = get_user_model()


def add_like(obj, user):
    """
    Adds like to 'obj'.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user
    )
    return like


def remove_like(obj, user):
    """
    Removes like from 'obj'.
    """
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user).delete()


def is_fan(obj, user) -> bool:
    """
    Checks whether the user liked 'obj'.
    """
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()