from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from .forms import AddMessageForm
from django.contrib.auth.decorators import login_required
from dashboard.models import Course
from enroll.models import Enrollment
from django.http import HttpResponse


def show_messages(request, course_id):
    parent_messages = Message.objects.filter(course__id=course_id).filter(parent_message__isnull=True)
    return render(request, 'notice_board/message_list.html', {'message_list': parent_messages,
                                                              'course_id': course_id})


@login_required()
def post_message(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.user.is_superuser:
        return HttpResponse("PMA admin cannot post messages", status=403)
    if request.user != course.owner:
        enrollment = Enrollment.objects.filter(user=request.user, course=course, status='apv').first()
        if not enrollment:
            return HttpResponse("You must be enrolled and approved to add assignment for this course.", status=403)
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.course = course
            message.save()
            return redirect('list-messages', course_id=course_id)
    else:
        form = AddMessageForm()
    return render(request, 'notice_board/post_message.html',
                      {'form': form})


@login_required()
def post_reply(request, course_id, message_id):
    parent_message = Message.objects.get(id=message_id)
    if request.method == 'POST':
        form = AddMessageForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.course_id = course_id
            reply.parent_message = parent_message
            reply.save()
            return redirect('message-detail', message_id)  # Adjust redirect as needed
    else:
        form = AddMessageForm()

    return render(request, 'notice_board/post_message.html', {'form': form, 'parent_message': parent_message})


def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    reply_messages = Message.objects.filter(parent_message=message)

    return render(request, 'notice_board/message_detail.html', {'message': message,
                                                                'reply_messages': reply_messages})