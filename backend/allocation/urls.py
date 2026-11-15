
from django.urls import path, re_path

from .views import (
    StudentRegistrationView,
    StudentLookupView,
    GroupListView,
    GroupDetailView,
    AdminStatsView,
)

urlpatterns = [
    path("register/", StudentRegistrationView.as_view(), name="student-register"),

    re_path(
        r"^student/(?P<index_number>.+)/$",
        StudentLookupView.as_view(),
        name="student-lookup",
    ),

    path("groups/", GroupListView.as_view(), name="group-list"),
    path("groups/<int:number>/", GroupDetailView.as_view(), name="group-detail"),
    path("admin/stats/", AdminStatsView.as_view(), name="admin-stats"),
]
