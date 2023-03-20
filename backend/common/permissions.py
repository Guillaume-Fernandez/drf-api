from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import connection
from rest_framework import permissions

def create_groups():
    """
        Create all groups needed. Is called at startup by AppConfig.ready
    """
    all_tables = connection.introspection.table_names()
    if 'auth_group' in all_tables:
        """
        Without this condition, you cannot generate completely new database (relation "auth_group" does not exist)
        """
        Group.objects.get_or_create(name='common_users')

class CommonUserPermission(permissions.BasePermission):
    def has_group(self, request, group):
        return request.user.groups.filter(name=group).exists()

    def has_permission(self, request, view):
        """
            The all() function returns True if all items in an iterable are true, otherwise it returns False.
        """
        return all([
            self.has_group(request, 'common_users'),
        ])