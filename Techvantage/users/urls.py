from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, FileUploadView, RetrieveFileView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('retrieve/<int:file_id>', RetrieveFileView.as_view(), name='file-retrieve'),
]
