from rest_framework import viewsets, renderers, views, response, authentication, permissions
from rest_framework.pagination import PageNumberPagination

from .renderers import CommonRenderer
from .permissions import CommonUserPermission

class LabsResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class LabsBaseViewSet(CommonUserPermission, viewsets.ModelViewSet):
    renderer_classes = [CommonRenderer, renderers.BrowsableAPIRenderer, renderers.JSONRenderer]
    pagination_class = LabsResultsSetPagination
    # permission_classes = [LabsUserPermission]
    # authentication_classes = [authentication.SessionAuthentication]


class DashboardAPIView(CommonUserPermission, views.APIView):
    name = 'SampleApp'
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.BrowsableAPIRenderer, renderers.JSONRenderer]
    template_name = 'common/dashboard.html'
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return the dashboard view.
        HTML => A description about the project and infrastructure status.
        API/JSON => Shorter description and infrastructure status.
        """

        return response.Response({
            'hi': 'Welcome at my-website.com.',
            'varA': 'You may want to print global information there',
        })