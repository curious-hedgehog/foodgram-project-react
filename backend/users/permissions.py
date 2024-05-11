from rest_framework.permissions import BasePermission


class IsAuthenticatedForMeEndpoint(BasePermission):

    def has_permission(self, request, view):
        if request.parser_context.get('view').action == 'me':
            return bool(request.user and request.user.is_authenticated)
        return True
