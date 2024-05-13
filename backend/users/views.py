from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from recipes.serializers import UserFollowingSerializer

User = get_user_model()


class FollowListView(generics.ListAPIView):
    """Вью-класс для списка подписок."""

    queryset = User.objects.all()
    serializer_class = UserFollowingSerializer

    def get_queryset(self):
        return self.request.user.followings.order_by('id')


class FollowCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    """Вью-класс для создания и удаления подписок."""

    serializer_class = UserFollowingSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(User, id=kwargs['user_id'])
        if follower == following or following in follower.followings.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follower.followings.add(following)
        serializer = self.get_serializer(following)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def delete(self, request, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(User, id=kwargs['user_id'])
        if follower == following or following not in follower.followings.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follower.followings.remove(following)
        return Response(status=status.HTTP_204_NO_CONTENT)
