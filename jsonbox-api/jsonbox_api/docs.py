from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly

DocumentationView = get_schema_view(
    openapi.Info(
        title="Json Box API",
        default_version="v1",
        description="jsonbox-api documentation page",
        license=openapi.License("MIT LICENSE"),
    ),
    public=True,
    permission_classes=(IsAuthenticatedOrReadOnly,),
)


class DocumentationRedirectView(RedirectView):
    url = reverse_lazy("documentation")
