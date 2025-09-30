from django.urls import path
from notifications.views import *

urlpatterns = [
    path("count", notification_count, name="notification-count"),
    path("<str:id>", retrieve_notification, name="retrieve-notification"),
    path("<str:id>", mark_notification, name="mark-notification"),
    path("", delete_all_notifications, name="delete-all-notifications"),
]
