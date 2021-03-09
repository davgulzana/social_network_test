from rest_framework.decorators import action
from rest_framework.response import Response

from post import utils


class LikedMixin:
    @action(methods=["POST"], detail=True)
    def like(self, request, uuid=None):
        """
        This action to like the object.
        """
        obj = self.get_object()
        utils.add_like(obj, request.user)
        return Response()

    @action(methods=["POST"], detail=True)
    def unlike(self, request, uuid=None):
        """
        This action to unlike the object.
        """
        obj = self.get_object()
        utils.remove_like(obj, request.user)
        return Response()
