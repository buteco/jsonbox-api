from django.conf.urls import include, url

from .docs import DocumentationRedirectView, DocumentationView

urlpatterns = [
    url(r"^v1/docs/", DocumentationView.with_ui("swagger"), name="documentation"),
    url(
        r"^v1/docs/swagger(?P<format>\.json|\.yaml)$",
        DocumentationView.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(r"^v1/", include("apps.jsons.routes")),
    url(r"^$", DocumentationRedirectView.as_view()),
]
