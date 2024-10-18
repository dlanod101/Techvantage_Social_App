from django.db import models
from users.models import CustomUser

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    
# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='project')
    title = models.CharField(max_length=250)
    content = models.TextField()
    contributors = models.ManyToManyField(CustomUser, related_name='contributed_project', blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)  # Must be defined
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class UploadedFile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='uploaded')  # Reference to the user
    file_name = models.CharField(max_length=255)
    file_url = models.URLField()  # To store the file URL
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} uploaded by {self.user}"