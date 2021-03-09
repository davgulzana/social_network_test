from datetime import datetime

from django.db.models import Count, Min, Q
from django.utils import timezone
from rest_framework import status, viewsets, permissions as p
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .mixins import LikedMixin
from .models import Post, Like
from .permissions import IsPostAuthor
from .serializers import PostSerializer, LikesAnalyticsSerializer


class PostViewSet(LikedMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "uuid"

    def get_serializer_context(self):
        return {"request": self.request}

    def get_permissions(self):
        if self.action in ["create", "own"]:
            permissions = [
                p.IsAuthenticated,
            ]
        elif self.action in ["update", "partial_update", "destroy"]:
            permissions = [IsPostAuthor]
        else:
            permissions = []
        return [permission() for permission in permissions]

    @action(detail=False, methods=["get"])
    def own(self, request, pk=None):
        """
        This action to get posts of user from request.
        """
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikesAnalytics(APIView):
    """
    View for get analytics about how many likes were made
    by the user in the period from 'date_from' to 'date_to'.
    If query parameter 'date_from' is empty, likes will be filtered from first like of the user.
    If query parameter 'date_to' is empty, likes will be filtered to current date.
    Result aggregated by day.
    """

    permission_classes = [p.IsAuthenticated]

    def get(self, request):
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get(
            "date_to", timezone.now().strftime("%Y-%m-%d")
        )
        end_date = datetime.strptime(date_to, "%Y-%m-%d").date()
        if date_from is None:
            start_date = (
                Like.objects.all()
                .aggregate(Min("created_at"))["created_at__min"]
                .date()
            )
        else:
            start_date = datetime.strptime(date_from, "%Y-%m-%d").date()
        res = (
            Like.objects.filter(
                Q(user=request.user) & Q(created_at__date__range=[start_date, end_date])
            )
            .values("created_at")
            .annotate(total_likes=Count("id"))
        )
        serializer = LikesAnalyticsSerializer(res, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
