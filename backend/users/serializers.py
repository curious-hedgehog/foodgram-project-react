from rest_framework import serializers
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

from api.models import Recipe

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    # password = serializers.CharField(write_only=True)
    # id = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())


    class Meta:
        model = User
        fields = ('email', 'username',
                  'first_name', 'last_name', 'password', 'id')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
        # write_only_fields = ()


class RecipeShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)



class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        follower = self.context['request'].user
        if not self.context['request'].user.is_authenticated:
            return False
        return follower.followings.filter(id=obj.id).exists()


class FollowingUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed', 'recipes', 'recipes_count',)

    def get_is_subscribed(self, obj):
        follower = self.context['request'].user
        return follower.followings.filter(id=obj.id).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes_limit_param = self.context.get('request').query_params.get('recipes_limit')
        if recipes_limit_param is None or not recipes_limit_param.isdigit():
            recipes = obj.recipes.all()
        else:
            recipes = obj.recipes.all()[:int(recipes_limit_param)]
        return RecipeShortSerializer(recipes, many=True).data
