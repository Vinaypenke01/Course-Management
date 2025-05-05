from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from .models import Course, Module, Lesson
from .serializers import CourseSerializer, ModuleSerializer, LessonSerializer

class CourseService:
    @staticmethod
    def get_all(page=1, per_page=10):
        queryset = Course.objects.all()
        paginator = Paginator(queryset, per_page)
        paginated_qs = paginator.get_page(page)
        return {
            'data': CourseSerializer(paginated_qs, many=True).data,
            'total_pages': paginator.num_pages,
            'current_page': page,
            
        }

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(Course, pk=pk)

    @staticmethod
    def create(data):
        serializer = CourseSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def update(pk, data):
        obj = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete(pk):
        obj = get_object_or_404(Course, pk=pk)
        obj.delete()


class ModuleService:
    @staticmethod
    def get_all(page=1, per_page=10):
        queryset = Module.objects.select_related('course').all()

        paginator = Paginator(queryset, per_page)
        paginated_qs = paginator.get_page(page)
        return {
            'data': ModuleSerializer(paginated_qs, many=True).data,
            'total_pages': paginator.num_pages,
            'current_page': page
        }

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(Module, pk=pk)

    @staticmethod
    def create(data):
        serializer = ModuleSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def update(pk, data):
        obj = get_object_or_404(Module, pk=pk)
        serializer = ModuleSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete(pk):
        obj = get_object_or_404(Module, pk=pk)
        obj.delete()


class LessonService:
    @staticmethod
    def get_all(page=1, per_page=5):
        queryset = Lesson.objects.all().order_by('-created_at')  # optional ordering
        paginator = Paginator(queryset, per_page)
        paginated_qs = paginator.get_page(page)
        return {
            'data': LessonSerializer(paginated_qs, many=True).data,
            'total_pages': paginator.num_pages,
            'current_page': page,
            'page_obj': paginated_qs  # ✅ added for template pagination
        }

    @staticmethod
    def get_by_id(pk):
        return get_object_or_404(Lesson, pk=pk)

    @staticmethod
    def create(data):
        serializer = LessonSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def update(pk, data):
        obj = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(obj, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    @staticmethod
    def delete(pk):
        obj = get_object_or_404(Lesson, pk=pk)
        obj.delete()
