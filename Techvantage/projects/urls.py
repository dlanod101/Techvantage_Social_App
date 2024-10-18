from django.urls import path
from . import views

urlpatterns = [
    # Project URLs
    path("projects/", views.ProjectViewSet.as_view({'get': 'list', 'post': 'create'}), name="project-list-create"),
    path("projects/<int:pk>/", views.ProjectRetrieveUpdateDestroy.as_view(), name="project-update-destroy"),
    path("projects_find/", views.ProjectFind.as_view(), name="project-find"),
    
    # Category URLs
    path("category/", views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name="category-list-create"),
    path("category/<int:pk>/", views.CategoryRetrieveUpdateDestroy.as_view(), name="category-update-destroy"),
    
    # Tag URLs
    path("tags/", views.TagViewSet.as_view({'get': 'list', 'post': 'create'}), name="tag-list-create"),
    path("tags/<int:pk>/", views.TagRetrieveUpdateDestroy.as_view(), name="tag-update-destroy"),

    path('upload/', views.FileUploadView.as_view(), name='file-upload'),
    path('retrieve/<int:file_id>', views.RetrieveFileView.as_view(), name='file-retrieve'),
]
