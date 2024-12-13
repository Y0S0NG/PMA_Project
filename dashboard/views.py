from datetime import datetime
from typing import Any
from django.forms import BaseModelForm, ValidationError
from django.http import FileResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib import messages
from dashboard.forms import AddAssignmentToCourseForm, AddCourseForm, CourseFileForm, FilterCourseFiles
from .models import Course, Assignment, UserSchedule, CourseFile
from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import get_object_or_404
import requests
from django.http import FileResponse
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from enroll.models import Enrollment


def user_schedule_view(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to schedule function")

    user_schedule, created = UserSchedule.objects.get_or_create(user=request.user)

    assignments = user_schedule.assignments.all()

    sorting_token = request.GET.get('sort_by', 'due_date')
    sorting_order = request.GET.get('order', 'asc')

    if sorting_order == 'asc':
        assignments = assignments.order_by(sorting_token)
    else:
        assignments = assignments.order_by(f'-{sorting_token}')

    return render(request, 'user_schedule.html', {'assignments': assignments})


def check_off_assignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    assignment.date_submitted = datetime.now()
    assignment.save()

    course = assignment.course_name
    enrollments = Enrollment.objects.filter(course=course, status='apv')

    for enrollment in enrollments:
        schedule, _ = UserSchedule.objects.get_or_create(user=enrollment.user)
        schedule.completed_assignments.add(assignment)
        schedule.assignments.remove(assignment)
        schedule.save()

    if course.owner:
        owner_schedule, _ = UserSchedule.objects.get_or_create(user=course.owner)
        owner_schedule.completed_assignments.add(assignment)
        owner_schedule.assignments.remove(assignment)
        owner_schedule.save()

    return redirect('schedule_view')


def delete_completed_assignment(request, assignment_id):
    user_schedule, created = UserSchedule.objects.get_or_create(user=request.user)
    assignment = Assignment.objects.get(pk=assignment_id)
    user_schedule.completed_assignments.remove(assignment)
    user_schedule.save()
    return redirect('user_schedule_complete')


def user_schedule_view_complete(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to schedule function")

    user_schedule, created = UserSchedule.objects.get_or_create(user=request.user)

    assignments = user_schedule.completed_assignments.all()

    sorting_token = request.GET.get('sort_by', 'due_date')
    sorting_order = request.GET.get('order', 'asc')

    if sorting_order == 'asc':
        assignments = assignments.order_by(sorting_token)
    else:
        assignments = assignments.order_by(f'-{sorting_token}')

    return render(request, 'user_schedule_complete.html', {'assignments': assignments})


class CourseIndexView(ListView):
    template_name = "dashboard/course_index.html"
    context_object_name = "course_list"

    def get_queryset(self):
        return Course.objects.order_by("name")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['username_startswith_guest'] = self.request.user.username.startswith('guest')
        context['pma_admin'] = self.request.user.is_superuser
        return context


@login_required()
def add_course(request):
    if request.user.username.startswith('guest'):
        return HttpResponseForbidden("Guest has no access to add course")
    if request.user.is_superuser:
        return HttpResponse("PMA admin user cannot create any course")
    if request.method == 'POST':
        form = AddCourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()
            return redirect('course_index')
    else:
        form = AddCourseForm()

    return render(request, 'dashboard/add_course.html', {'form': form})


@login_required()
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user != course.owner and not request.user.is_superuser:
        return HttpResponseForbidden('You have no permission to delete this file')
    course.delete()
    messages.success(request, 'Course deleted successfully.')
    return redirect('course_index')


def add_assignment_view(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.is_superuser:
        return HttpResponse("PMA admin cannot add assignments", status=403)

    if request.user != course.owner:
        enrollment = Enrollment.objects.filter(user=request.user, course=course, status='apv').first()
        if not enrollment:
            return HttpResponse("You must be enrolled and approved to add assignment for this course.", status=403)

    if request.method == "POST":
        assignmentForm = AddAssignmentToCourseForm(request.POST)
        if assignmentForm.is_valid():
            data = assignmentForm.data
            file = request.FILES.get('file')
            a = Assignment(course_name=course, description=data['description'], assignment_type=data['assignment_type'],
                           due_date=data['due_date'], priority=data['priority'], keywords=data['keywords'],
                           date_submitted=timezone.now()  # Set date_submitted to current timestamp explicitly
                           )
            a.save()

            return redirect('course_detail', pk=course_id)
    else:
        assignmentForm = AddAssignmentToCourseForm()
    return render(request, 'dashboard/course_assignment_add.html',
                  {'course_id': course_id, 'course': course, 'Aform': assignmentForm})


class CourseDetailView(DetailView):
    model = Course
    template_name = 'dashboard/course_detail.html'  # Ensure this is your correct template

    def get_assignments(self):
        course_name = self.get_object()
        return Assignment.objects.filter(course_name=course_name)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        search_term = self.request.GET.get('search', '')
        file_search_term = self.request.GET.get('file_search', '')
        assignments = Assignment.objects.filter(course_name=self.object)
        course_files = CourseFile.objects.filter(course=self.object)
        if search_term:
            assignments = assignments.filter(
                keywords__icontains=search_term
            )
        if file_search_term:
            matched_types = [code for code, desc in CourseFile.CONTENT_TYPE_CHOICES if
                             file_search_term.lower() in desc.lower()]

            course_files = course_files.filter(
                Q(keywords__icontains=file_search_term) | Q(content_type__in=matched_types)
            )

        context['course_files'] = course_files
        context['assignments'] = assignments
        context['search_term'] = search_term
        context['pma_admin'] = self.request.user.is_superuser

        return context

    # Override the post method to allow for the import of stuff
    def post(self, request, *args, **kwards):
        course_name = self.get_object()
        assignments = Assignment.objects.filter(course_name=course_name)
        user_schedule, created = UserSchedule.objects.get_or_create(user=request.user)
        user_schedule.assignments.add(*assignments)
        user_schedule.save()
        messages.success(request, 'Assignments have been successfully imported to your schedule.')
        return redirect('course_detail', pk=course_name.id)


def check_course_ownership(user, course_id):
    try:
        course = Course.objects.get(id=course_id, owner=user)
    except Course.DoesNotExist:
        raise PermissionDenied("You do not have permission to access this course.")
    return course

      
def upload_course_file(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.is_superuser:
        return HttpResponse("PMA admin user cannot upload course file", status=403)

    if request.user != course.owner:
        enrollment = Enrollment.objects.filter(user=request.user, course=course, status='apv').first()
        if not enrollment:
            return HttpResponse("You must be enrolled and approved to upload files for this course.", status=403)

    if request.method == 'POST':
        form = CourseFileForm(request.POST, request.FILES)
        if form.is_valid():
            course_file = form.save(commit=False)
            course_file.course = course
            course_file.uploaded_by = request.user
            file_type = course_file.file.name.split('.')[-1].lower()
            course_file.file_type = file_type
            course_file.save()
            messages.success(request, 'File uploaded successfully.')
            return redirect('upload_course_file', course_id=course.id)
        else:
            for field in form.errors:
                existing_classes = form[field].field.widget.attrs.get('class', '')
                form[field].field.widget.attrs['class'] = f'{existing_classes} is-invalid'
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CourseFileForm()

    return render(request, 'dashboard/upload_course_file.html', {'form': form, 'course': course})


def delete_course_file(request, file_id):
    file = CourseFile.objects.get(id=file_id)
    course = file.course
    file.delete()
    messages.success(request, 'File deleted successfully.')
    return redirect('course_detail', pk=course.id)


def upload_course_image(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            course.course_image = image
            course.save()
            messages.success(request, 'Course image uploaded successfully!')
        else:
            messages.error(request, 'No image was uploaded.')
        return redirect('course_detail', pk=course.id)

    return redirect('course_detail', pk=course.id)


def view_course_file(request, file_id):
    course_file = get_object_or_404(CourseFile, pk=file_id)

    file_response = requests.get(course_file.file.url, stream=True)

    content_disposition = 'inline' if course_file.file_type in ['pdf', 'jpg', 'png', 'txt'] else 'attachment'

    response = FileResponse(file_response.raw, as_attachment=(content_disposition == 'attachment'))
    response['Content-Type'] = file_response.headers['Content-Type']
    response['Content-Disposition'] = f"{content_disposition}; filename=\"{course_file.file.name}\""

    return response


def course_file_search(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course_files = CourseFile.objects.filter(course=course)
    form = FilterCourseFiles
    if request.method == 'POST':
        form = FilterCourseFiles(request.POST)
        data = form.data
        name = data['filename']
        content_type = data['content_type']
        keywords = data['keywords']
        if content_type:
            course_files = course_files.filter(content_type=content_type)
        if name:
            course_files = course_files.filter(filename__icontains=name)
        if keywords:
            keyword_list = [keyword.strip() for keyword in keywords.split(',')]
            query = Q()
            for keyword in keyword_list:
                query |= Q(keywords__icontains=keyword)  # Create an OR condition for each keyword

            course_files = course_files.filter(query)  # Apply the keyword filter
    return render(request, 'dashboard/course_file_search.html', {
        'course': course,
        'files': course_files,
        'form': form
    })