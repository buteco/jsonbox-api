from rest_framework import routers

from .api import JsonViewSet

app_name = "jsons"
router = routers.DefaultRouter()
router.register(r"jsons", JsonViewSet, basename="jsons")
urlpatterns = router.urls
