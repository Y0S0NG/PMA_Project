from django.urls import include, path
from .views import (add_assignment_view, check_off_assignment, delete_completed_assignment, user_schedule_view, CourseDetailView, CourseIndexView, add_course, upload_course_file,
                    upload_course_image, user_schedule_view_complete, view_course_file, delete_course_file,
                    course_file_search, delete_course)

urlpatterns = [
    path('assignments/', user_schedule_view, name='schedule_view'),
    path('assignments/complete', user_schedule_view_complete, name='user_schedule_complete'),
    path('assignments/complete/delete/<int:assignment_id>', delete_completed_assignment, name='delete_completed'),
    path('assignments/submit/<int:assignment_id>', check_off_assignment, name='turn_in'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('course/<int:course_id>/delete', delete_course, name='course_delete'),
    path('course/<int:course_id>/add', add_assignment_view, name='course_assignment_add'),
    path('course/', CourseIndexView.as_view(), name='course_index'),
    path('course/add', add_course, name='course_add'),
    path('course/<int:course_id>/upload/', upload_course_file, name='upload_course_file'),
    path('course/<int:course_id>/upload_image/', upload_course_image, name='upload_course_image'),
    path('files/<int:file_id>/', view_course_file, name='view_course_file'),
    path('course-file/delete/<int:file_id>/', delete_course_file, name='delete_course_file'),
    path('course/<int:course_id>/course_file_search/', course_file_search, name='search_course_file'),
    path("", include("login.urls")),
]