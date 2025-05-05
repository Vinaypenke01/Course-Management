from django.urls import path
import uuid
from .views import (
    CourseListView, CourseCreateView, CourseUpdateView, CourseDeleteView,
    ModuleListView, ModuleCreateView, ModuleUpdateView, ModuleDeleteView,
    LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView
)

urlpatterns = [

    # Course URLs
    path('', CourseListView.as_view(), name='course-list'),
    path('courses/create/', CourseCreateView.as_view(), name='course-create'),
    path('courses/update/<uuid:pk>/', CourseUpdateView.as_view(), name='course-update'),
    path('courses/delete/<uuid:pk>/', CourseDeleteView.as_view(), name='course-delete'),

    # Module URLs
    path('modules/', ModuleListView.as_view(), name='module-list'),
    path('modules/create/', ModuleCreateView.as_view(), name='module-create'),
    path('modules/update/<uuid:pk>/', ModuleUpdateView.as_view(), name='module-update'),
    path('modules/delete/<uuid:pk>/', ModuleDeleteView.as_view(), name='module-delete'),

    # Lesson URLs
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/update/<uuid:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/delete/<uuid:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),

]
