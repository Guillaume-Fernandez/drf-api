from django.contrib.auth.models import Group
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

def create_groups():
    """
        Create all groups needed. Is called at startup by AppConfig.ready
    """
    Group.objects.get_or_create(name='common_users')

# LoginRequiredMixin is used to authenticate users and redirect them to the login page if need.
# IMPORTANT: LoginRequiredMixin should be at the leftmost position in the inheritance list.
# Doc: https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-loginrequiredmixin-mixin

# PermissionRequiredMixin is not used because the application does not need such details.
# UserPassesTestMixin is used instead to do a simple and minimalist check in user's groups.
# Doc: https://docs.djangoproject.com/en/4.1/topics/auth/default/#django.contrib.auth.mixins.UserPassesTestMixin

class CommonUserPermission(LoginRequiredMixin, UserPassesTestMixin):
    def has_group(self, group):
        return self.request.user.groups.filter(name=group).exists()

    def test_func(self):
        """
            The all() function returns True if all items in an iterable are true, otherwise it returns False.
        """
        return all([
            self.has_group('common_users'),
        ])

