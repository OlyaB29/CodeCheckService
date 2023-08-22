from django.urls import path

from . import views

app_name = 'check_app'

urlpatterns = [
    path("sign-up/", views.SignUp.as_view(), name="sign-up"),
    path("", views.FileCreateView.as_view(), name="home"),
    path("files", views.FileListView.as_view(), name="files"),
    path("update-file/<int:pk>", views.FileUpdateView.as_view(), name="update-file"),
    path("delete-file/<int:pk>", views.FileDeleteView.as_view(), name="delete-file"),
    path("<int:file_id>/logs", views.LogListView.as_view(), name="file-logs"),
]
