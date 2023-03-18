from rest_framework import viewsets, renderers, views, response, authentication, permissions
from rest_framework.pagination import PageNumberPagination
import django.urls.resolvers

from k8s.utils import list_ns_with_status
import labs.urls  
from .renderers import LabsRenderer
from .permissions import LabsUserPermission

class LabsResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LabsBaseViewSet(LabsUserPermission, viewsets.ModelViewSet):
    renderer_classes = [LabsRenderer, renderers.BrowsableAPIRenderer, renderers.JSONRenderer]
    pagination_class = LabsResultsSetPagination
    # permission_classes = [LabsUserPermission]
    # authentication_classes = [authentication.SessionAuthentication]


class DashboardAPIView(LabsUserPermission, views.APIView):
    name = 'Labs'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.BrowsableAPIRenderer, renderers.JSONRenderer]
    template_name = 'labs_common/dashboard.html'
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return the dashboard view.
        HTML => A description about the project and infrastructure status.
        API/JSON => Shorter description and infrastructure status.
        """

        environments, nb_envs_running = list_ns_with_status()
        return response.Response({
            'hi': 'Welcome at labs.open-prod.com. The labs is a project aiming to automate recurring system tasks.',
            'environments': environments,
            'nb_envs_running': nb_envs_running,
        })