from django.views import View
from django.shortcuts import render, redirect
from .services import *
from django.core.exceptions import ValidationError
from uuid import UUID
from django.views.generic import ListView


# ---------- COURSE VIEWS ----------
class CourseListView(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        result = CourseService.get_all(page=int(page))
        return render(request, 'core/course_list.html', {
    'courses': result['data'],
    'total_pages': result['total_pages'],
    'current_page': result['current_page'],
})



class CourseCreateView(View):
    def get(self, request):
        return render(request, 'core/course_form.html')

    def post(self, request):
        data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'duration' :request.POST.get('duration')
        }
        CourseService.create(data)
        return redirect('course-list')


class CourseUpdateView(View):
    def get(self, request, pk):
        course = CourseService.get_by_id(pk)
        return render(request, 'core/course_form.html', {'course': course})

    def post(self, request, pk):
        data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'duration' :request.POST.get('duration')
        }
        CourseService.update(pk, data)
        return redirect('course-list')


class CourseDeleteView(View):
    def get(self, request, pk):
        course = CourseService.get_by_id(pk)
        return render(request, 'core/course_confirm_delete.html', {'course': course})

    def post(self, request, pk):
        CourseService.delete(pk)
        return redirect('course-list')


# ---------- MODULE VIEWS ----------
class ModuleListView(ListView):
    model = Module
    template_name = 'core/module_list.html'
    context_object_name = 'modules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        per_page = 10
        module_data = ModuleService.get_all(page, per_page)
        context['modules'] = module_data['data']  # This will now include course_name due to the serializer
        return context



class ModuleCreateView(View):
    def get(self, request):
        courses = CourseService.get_all()['data']
        return render(request, 'core/module_form.html', {'courses': courses})

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        course_id = request.POST.get('course')  # This comes from the HTML form

        # Validate and fetch Course object using UUID
        try:
            course = Course.objects.get(pk=UUID(course_id))
        except (Course.DoesNotExist, ValueError, ValidationError):
            return redirect('error-page')  # Or return an error message

        data = {
            'title': title,
            'description': description,
            'course': course_id,  # Pass UUID, not object if your serializer expects ID
        }

        ModuleService.create(data)
        return redirect('module-list')
class ModuleUpdateView(View):
    def get(self, request, pk):
        module = ModuleService.get_by_id(pk)
        courses = CourseService.get_all()['data']
        return render(request, 'core/module_form.html', {'module': module, 'courses': courses})

    def post(self, request, pk):
        data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'course': request.POST.get('course')
        }
        ModuleService.update(pk, data)
        return redirect('module-list')


class ModuleDeleteView(View):
    def get(self, request, pk):
        module = ModuleService.get_by_id(pk)
        return render(request, 'core/module_confirm_delete.html', {'module': module})

    def post(self, request, pk):
        ModuleService.delete(pk)
        return redirect('module-list')


# ---------- LESSON VIEWS ----------
class LessonListView(ListView):
    model = Lesson
    template_name = 'core/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 5  # Number of lessons per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get('page', 1)
        per_page = self.paginate_by  # Use paginate_by to decide how many items per page
        lesson_data = LessonService.get_all(page, per_page)

        # Provide the lessons data and the page_obj for pagination
        context['lessons'] = lesson_data['data']  # Lessons data for the current page
        context['page_obj'] = lesson_data['page_obj']  # Pagination info for the template

        return context

class LessonCreateView(View):
    def get(self, request):
        modules = ModuleService.get_all()['data']
        return render(request, 'core/lesson_form.html', {'modules': modules})

    def post(self, request):
        data = {
            'title': request.POST.get('title'),
            'content':request.POST.get('content'),
            'video_url': request.POST.get('video_url'),
            'module': request.POST.get('module')
        }
        LessonService.create(data)
        return redirect('lesson-list')


class LessonUpdateView(View):
    def get(self, request, pk):
        lessons = LessonService.get_by_id(pk)
        modules = ModuleService.get_all()['data']
        return render(request, 'core/lesson_form.html', {'lessons': lessons, 'modules': modules})

    def post(self, request, pk):
        data = {
            'title': request.POST.get('title'),
            'content':request.POST.get('content'),
            'video_url': request.POST.get('video_url'),
            'module': request.POST.get('module')
        }
        LessonService.update(pk, data)
        return redirect('lesson-list')


class LessonDeleteView(View):
    def get(self, request, pk):
        lesson = LessonService.get_by_id(pk)
        return render(request, 'core/lesson_confirm_delete.html', {'lesson': lesson})

    def post(self, request, pk):
        LessonService.delete(pk)
        return redirect('lesson-list')
