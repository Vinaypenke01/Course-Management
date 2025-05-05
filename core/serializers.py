from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'





class ModuleSerializer(serializers.ModelSerializer):
    sequence_order = serializers.IntegerField(required=False, default=1)
    course_name = serializers.CharField(source='course.name', read_only=True)  # Add the related course name
    class Meta:
        model = Module
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)  # Add the related module title
    course_title = serializers.CharField(source='module.course.name', read_only=True)  # Add the related course title via module
    class Meta:
        model = Lesson
        fields = '__all__'
