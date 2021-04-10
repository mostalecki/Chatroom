from src.apps.chat import views

from rest_framework.routers import SimpleRouter

room_router = SimpleRouter()
room_router.register("rooms", views.RoomViewSet, basename="rooms")

urlpatterns = [] + room_router.urls
