from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError, NotFound
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer


class CourseService:
    @staticmethod
    def get_all(page=1, per_page=10):
        try:
            queryset = Course.objects.all()
            paginator = Paginator(queryset, per_page)
            paginated_qs = paginator.get_page(page)
            return {
                'data': CourseSerializer(paginated_qs, many=True).data,
                'total_pages': paginator.num_pages,
                'current_page': page,
            }
        except (PageNotAnInteger, EmptyPage) as e:
            raise ValidationError({"error": "Invalid page number", "details": str(e)})
        except Exception as e:
            raise ValidationError({"error": "Failed to fetch courses", "details": str(e)})

    @staticmethod
    def get_by_id(pk):
        try:
            return get_object_or_404(Course, pk=pk)
        except Exception as e:
            raise NotFound({"error": "Course not found", "details": str(e)})

    @staticmethod
    def create(data):
        try:
            serializer = CourseSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Course creation failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during course creation", "details": str(e)})

    @staticmethod
    def update(pk, data):
        try:
            obj = get_object_or_404(Course, pk=pk)
            serializer = CourseSerializer(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Course update failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during course update", "details": str(e)})

    @staticmethod
    def delete(pk):
        try:
            obj = get_object_or_404(Course, pk=pk)
            obj.delete()
        except Exception as e:
            raise ValidationError({"error": "Failed to delete course", "details": str(e)})


class ModuleService:
    @staticmethod
    def get_all(page=1, per_page=20):
        try:
            queryset = Module.objects.select_related('course').all()
            paginator = Paginator(queryset, per_page)
            paginated_qs = paginator.get_page(page)
            return {
                'data': ModuleSerializer(paginated_qs, many=True).data,
                'total_pages': paginator.num_pages,
                'current_page': page
            }
        except (PageNotAnInteger, EmptyPage) as e:
            raise ValidationError({"error": "Invalid page number", "details": str(e)})
        except Exception as e:
            raise ValidationError({"error": "Failed to fetch modules", "details": str(e)})

    @staticmethod
    def get_by_id(pk):
        try:
            return get_object_or_404(Module, pk=pk)
        except Exception as e:
            raise NotFound({"error": "Module not found", "details": str(e)})

    @staticmethod
    def create(data):
        try:
            serializer = ModuleSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Module creation failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during module creation", "details": str(e)})

    @staticmethod
    def update(pk, data):
        try:
            obj = get_object_or_404(Module, pk=pk)
            serializer = ModuleSerializer(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Module update failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during module update", "details": str(e)})

    @staticmethod
    def delete(pk):
        try:
            obj = get_object_or_404(Module, pk=pk)
            obj.delete()
        except Exception as e:
            raise ValidationError({"error": "Failed to delete module", "details": str(e)})


class LessonService:
    @staticmethod
    def get_all(page=1, per_page=5):
        try:
            queryset = Lesson.objects.all().order_by('-created_at')
            paginator = Paginator(queryset, per_page)
            paginated_qs = paginator.get_page(page)
            return {
                'data': LessonSerializer(paginated_qs, many=True).data,
                'total_pages': paginator.num_pages,
                'current_page': page,
                'page_obj': paginated_qs
            }
        except (PageNotAnInteger, EmptyPage) as e:
            raise ValidationError({"error": "Invalid page number", "details": str(e)})
        except Exception as e:
            raise ValidationError({"error": "Failed to fetch lessons", "details": str(e)})

    @staticmethod
    def get_by_id(pk):
        try:
            return get_object_or_404(Lesson, pk=pk)
        except Exception as e:
            raise NotFound({"error": "Lesson not found", "details": str(e)})

    @staticmethod
    def create(data):
        try:
            serializer = LessonSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Lesson creation failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during lesson creation", "details": str(e)})

    @staticmethod
    def update(pk, data):
        try:
            obj = get_object_or_404(Lesson, pk=pk)
            serializer = LessonSerializer(obj, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.data
        except ValidationError as e:
            raise ValidationError({"error": "Lesson update failed", "details": e.detail})
        except Exception as e:
            raise ValidationError({"error": "Unexpected error during lesson update", "details": str(e)})

    @staticmethod
    def delete(pk):
        try:
            obj = get_object_or_404(Lesson, pk=pk)
            obj.delete()
        except Exception as e:
            raise ValidationError({"error": "Failed to delete lesson", "details": str(e)})
