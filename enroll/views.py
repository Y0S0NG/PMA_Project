from django.shortcuts import render, get_object_or_404, redirect
from dashboard.models import Course, Assignment, UserSchedule
from django.http import HttpResponse, HttpResponseForbidden
from .models import Enrollment
from django.contrib.auth.decorators import login_required
from django.contrib import messages



@login_required()
def enroll(request, course_id):
    if request.user.is_superuser:
        return HttpResponse("PMA admin user cannot enroll in any class")
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )
    if created:
        enrollment.status = 'ude'
        enrollment.save()
        messages.success(request, 'Enrollment request send successfully, wait for course owner to approve')
        return redirect('course_index')
    else:
        if enrollment.status == 'ude':
            return HttpResponse("Your enrollment request is still under examination.", status=400)
        elif enrollment.status == 'apv':
            return HttpResponse("You are already enrolled in this course.", status=400)
        elif enrollment.status == 'rjt':
            return HttpResponse("Your enrollment request was rejected.", status=400)


@login_required()
def list_enrollment_requests(request):
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to schedule function")
    pending_enrollments = Enrollment.objects.filter(
        course__owner=request.user,
        status='ude'
    )

    return render(request, 'enroll/enrollment_requests.html', {'pending_enrollments': pending_enrollments})


@login_required()
def approve_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if enrollment.course.owner != request.user:
        return HttpResponse("You do not have permission to approve this enrollment.", status=403)

    enrollment.status = 'apv'
    enrollment.save()

    assignments = Assignment.objects.filter(course_name=enrollment.course)
    user_schedule, created = UserSchedule.objects.get_or_create(user=enrollment.user)
    user_schedule.assignments.add(*assignments)
    user_schedule.save()

    messages.success(request, "you've successfully approved an enrollment request")
    return redirect('enrollment_requests')


@login_required()
def reject_enrollment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if enrollment.course.owner != request.user:
        return HttpResponse("You do not have permission to approve this enrollment.", status=403)

    enrollment.status = 'rjt'
    enrollment.save()
    messages.success(request, "you've rejected an enrollment request")
    return redirect('enrollment_requests')


@login_required()
def enrolled_courses(request):
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to schedule function")
    approved_enrollments = Enrollment.objects.filter(user=request.user, status='apv')
    enrolled_courses = [enrollment.course for enrollment in approved_enrollments]

    return render(request, 'enroll/enrolled_courses.html', {'enrolled_courses': enrolled_courses})


@login_required()
def drop(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    enrollment.delete()
    messages.success(request, "successfully drop the course")
    return redirect('enrolled_courses')

@login_required()
def owned_courses(request):
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to schedule function")
    owned_courses = Course.objects.filter(owner=request.user)

    return render(request, 'enroll/owned_courses.html', {'owned_courses': owned_courses})

