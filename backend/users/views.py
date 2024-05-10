from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .serializers import UserSerializer, UserCreateSerializer, FollowingUserSerializer

User = get_user_model()


class ListCreateRetrieveMixin(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    pass

class UserViewSet(ListCreateRetrieveMixin):
    """Вью-класс для пользователей."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserSerializer
        return UserCreateSerializer


class FollowListView(generics.ListAPIView):
    """Вью-класс для списка подписок."""

    queryset = User.objects.all()
    serializer_class = FollowingUserSerializer

    def get_queryset(self):
        return self.request.user.followings.order_by('id')


class FollowCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    """Вью-класс для создания и удаления подписок."""

    serializer_class = FollowingUserSerializer
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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        follower = request.user
        following = get_object_or_404(User, id=kwargs['user_id'])
        if follower == following or following not in follower.followings.all():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follower.followings.remove(following)
        return Response(status=status.HTTP_204_NO_CONTENT)



