from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.ProjectListCreate.as_view(), name="project-view-create"),
    path(
        "projects/<int:pk>", 
         views.ProjectRetrieveUpdateDestroy.as_view(), 
         name="update"
         ),
    path("projects_list/", views.ProjectList.as_view(), name="project-list")
]