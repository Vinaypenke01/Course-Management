from django.views import View
from django.shortcuts import render, redirect
from .services import *
from django.core.exceptions import ValidationError
from uuid import UUID
from django.views.generic import ListView


# ---------- COURSE VIEWS ----------
from django.views import View
from django.shortcuts import render, redirect
from .services import *
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from uuid import UUID
from django.views.generic import ListView


# ---------- COURSE VIEWS ----------
class CourseListView(View):
    def get(self, request):
        try:
            page = request.GET.get('page', 1)
            result = CourseService.get_all(page=int(page))
            return render(request, 'core/course_list.html', {
                'courses': result['data'],
                'total_pages': result['total_pages'],
                'current_page': result['current_page'],
            })
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class CourseCreateView(View):
    def get(self, request):
        return render(request, 'core/course_form.html')

    def post(self, request):
        try:
            data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'duration': request.POST.get('duration')
            }
            CourseService.create(data)
            return redirect('course-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class CourseUpdateView(View):
    def get(self, request, pk):
        try:
            course = CourseService.get_by_id(pk)
            return render(request, 'core/course_form.html', {'course': course})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            data = {
                'name': request.POST.get('name'),
                'description': request.POST.get('description'),
                'duration': request.POST.get('duration')
            }
            CourseService.update(pk, data)
            return redirect('course-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class CourseDeleteView(View):
    def get(self, request, pk):
        try:
            course = CourseService.get_by_id(pk)
            return render(request, 'core/course_confirm_delete.html', {'course': course})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            CourseService.delete(pk)
            return redirect('course-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


# ---------- MODULE VIEWS ----------
class ModuleListView(ListView):
    model = Module
    template_name = 'core/module_list.html'
    context_object_name = 'modules'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page = self.request.GET.get('page', 1)
            per_page = 20
            module_data = ModuleService.get_all(page, per_page)
            context['modules'] = module_data['data']
        except Exception as e:
            context['error'] = str(e)
        return context


class ModuleCreateView(View):
    def get(self, request):
        try:
            courses = CourseService.get_all()['data']
            return render(request, 'core/module_form.html', {'courses': courses})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request):
        try:
            title = request.POST.get('title')
            description = request.POST.get('description')
            course_id = request.POST.get('course')

            try:
                course = Course.objects.get(pk=UUID(course_id))
            except (Course.DoesNotExist, ValueError, ValidationError):
                return redirect('error-page')

            data = {
                'title': title,
                'description': description,
                'course': course_id,
            }
            ModuleService.create(data)
            return redirect('module-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class ModuleUpdateView(View):
    def get(self, request, pk):
        try:
            module = ModuleService.get_by_id(pk)
            courses = CourseService.get_all()['data']
            return render(request, 'core/module_form.html', {'module': module, 'courses': courses})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            data = {
                'title': request.POST.get('title'),
                'description': request.POST.get('description'),
                'course': request.POST.get('course')
            }
            ModuleService.update(pk, data)
            return redirect('module-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class ModuleDeleteView(View):
    def get(self, request, pk):
        try:
            module = ModuleService.get_by_id(pk)
            return render(request, 'core/module_confirm_delete.html', {'module': module})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            ModuleService.delete(pk)
            return redirect('module-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


# ---------- LESSON VIEWS ----------
class LessonListView(ListView):
    model = Lesson
    template_name = 'core/lesson_list.html'
    context_object_name = 'lessons'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            page = self.request.GET.get('page', 1)
            per_page = self.paginate_by
            lesson_data = LessonService.get_all(page, per_page)
            context['lessons'] = lesson_data['data']
            context['page_obj'] = lesson_data['page_obj']
        except Exception as e:
            context['error'] = str(e)
        return context


class LessonCreateView(View):
    def get(self, request):
        try:
            modules = ModuleService.get_all()['data']
            return render(request, 'core/lesson_form.html', {'modules': modules})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request):
        try:
            data = {
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'video_url': request.POST.get('video_url'),
                'module': request.POST.get('module')
            }
            LessonService.create(data)
            return redirect('lesson-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class LessonUpdateView(View):
    def get(self, request, pk):
        try:
            lessons = LessonService.get_by_id(pk)
            modules = ModuleService.get_all()['data']
            return render(request, 'core/lesson_form.html', {'lessons': lessons, 'modules': modules})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            data = {
                'title': request.POST.get('title'),
                'content': request.POST.get('content'),
                'video_url': request.POST.get('video_url'),
                'module': request.POST.get('module')
            }
            LessonService.update(pk, data)
            return redirect('lesson-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})


class LessonDeleteView(View):
    def get(self, request, pk):
        try:
            lesson = LessonService.get_by_id(pk)
            return render(request, 'core/lesson_confirm_delete.html', {'lesson': lesson})
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})

    def post(self, request, pk):
        try:
            LessonService.delete(pk)
            return redirect('lesson-list')
        except Exception as e:
            return render(request, 'core/error.html', {'error': str(e)})
