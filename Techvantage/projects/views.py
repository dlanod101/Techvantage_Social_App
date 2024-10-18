from django.shortcuts import render
from users.models import CustomUser
from .models import Project, Category, Tag
from .serializers import ProjectSerializer, CategorySerializer, TagSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from django.db.models import Q  # Import Q object for complex queries
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# --- Project Views ---

# Project ViewSet for general CRUD operations
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        serializer.save(user=self.request.user)

# Retrieve, Update, Destroy view for a single project
class ProjectRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = "pk"

# Custom Project Finder API
class ProjectFind(APIView):
    def get(self, request, format=None):
        """
        Available query parameters:
        
        1. `/projects_find/?category=<category>` -- Finds all projects with that category
        2. `/projects_find/?tag=<tag>` -- Finds all projects with that tag
        3. `/projects_find/?contributors=<contributors>` -- Finds all projects with that contributor
        4. `/projects_find/` -- Displays all available projects
        """
        # Retrieve query parameters
        tag = request.query_params.get("tag", "")
        category = request.query_params.get("category", "")
        contributors = request.query_params.get("contributors", "")

        # Build query filters using Q objects
        filters = Q()
        
        if category:
            filters &= Q(categories__name__icontains=category)  # Assuming 'categories' is a many-to-many relation
        
        if tag:
            filters &= Q(tags__name__icontains=tag)  # Filter by tag name

        if contributors:
            filters &= Q(contributors__username__icontains=contributors)  # Contributors should be User model instances

        # Apply filters if any, otherwise return all projects
        projects = Project.objects.filter(filters) if filters else Project.objects.all()

        # Serialize the filtered projects and return the response
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Category Views ---

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'


# --- Tag Views ---

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'pk'



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedFile  # Your model for storing file URLs
import mimetypes
import firebase_admin
from firebase_admin import storage
from rest_framework.permissions import IsAuthenticated
from utilities.firebase import upload_app_file 

class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically detect content type
        mime_type, encoding = mimetypes.guess_type(file.name)
        content_type = mime_type if mime_type else 'application/octet-stream'

        try:
            # Upload the file to Firebase and get the public URL
            file_url = upload_app_file(file, 'project')

            # Save the file URL and associate it with the logged-in user
            uploaded_file = UploadedFile.objects.create(
                user=request.user,  # Associate with the logged-in user
                file_name=file.name,
                file_url=file_url
            )

            return Response({"message": "File uploaded successfully.", "file_url": uploaded_file.file_url}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def upload_file_to_firebase(file, content_type):
    # Assuming Firebase storage is initialized
    bucket = firebase_admin.storage.bucket()

    # Create a blob for the file
    blob = bucket.blob(f"uploads/{file.name}")

    # Upload the file and set the content type
    blob.upload_from_file(file, content_type=content_type)

    # Make the file publicly accessible
    blob.make_public()

    # Return the public URL of the uploaded file
    return blob.public_url



from .models import UploadedFile
from django.shortcuts import get_object_or_404

class RetrieveFileView(APIView):
    """
    View to retrieve file URLs stored in Firebase.
    """

    def get(self, request, file_id):
        # Fetch the file object using its ID
        file_obj = get_object_or_404(UploadedFile, id=file_id)

        # Retrieve the file URL from the database
        file_url = file_obj.file_url

        # Return the file URL in the response
        return Response({"file_url": file_url}, status=status.HTTP_200_OK)
