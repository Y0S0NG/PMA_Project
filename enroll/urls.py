from django.urls import path
from . import views

urlpatterns = [
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),
    path('enrollment_requests/', views.list_enrollment_requests, name='enrollment_requests'),
    path('approve_enrollment/<int:enrollment_id>/', views.approve_enrollment, name='approve_enrollment'),
    path('reject_enrollment/<int:enrollment_id>/', views.reject_enrollment, name='reject_enrollment'),
    path('enrolled_courses/', views.enrolled_courses, name='enrolled_courses'),
    path('drop/<int:course_id>/', views.drop, name='drop'),
    path('owned_courses/', views.owned_courses, name='owned_courses'),
]