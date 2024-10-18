from rest_framework import serializers
from .models import Project, Category, Tag
from users.models import CustomUser

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


from rest_framework import serializers
from .models import Project, Category, Tag
from users.models import CustomUser  # Assuming you have a User model

from rest_framework import serializers
from .models import Project, Category, Tag
from users.models import CustomUser  # Assuming you have a User model

class ProjectSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # ForeignKey for category
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)  # Many-to-Many for tags
    contributors = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), many=True, required=False)  # Many-to-Many for contributors

    class Meta:
        model = Project
        fields = ['id', 'title', 'content', 'category', 'tags', 'contributors', 'user']
        read_only_fields = ['user']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])  # Pop out tags
        contributors = validated_data.pop('contributors', [])  # Pop out contributors
        user = validated_data.pop('user', None)  # Pop out author, should be None since it's not in the payload
        project = Project.objects.create(user=user, **validated_data)  # Create project instance

        # Set the Many-to-Many relationship for tags and contributors
        project.tags.set(tags)  # Use set() for Many-to-Many fields
        project.contributors.set(contributors)  # Use set() for Many-to-Many fields
        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)  # Handle tags for updates
        contributors = validated_data.pop('contributors', None)  # Handle contributors for updates
        super().update(instance, validated_data)  # Update other fields

        # Update Many-to-Many relationships for tags and contributors
        if tags is not None:
            instance.tags.set(tags)  # Use set() for Many-to-Many fields
        if contributors is not None:
            instance.contributors.set(contributors)  # Use set() for Many-to-Many fields

        return instance
