from django.shortcuts import render, get_object_or_404, redirect
from notifications.signals import notify
from django.contrib.auth.models import User
from notifications.models import Notification
from notifications.utils import id2slug, slug2id
from django.contrib.auth.decorators import login_required
from .serializers import NotificationSerializer
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.template.loader import render_to_string
from django.http import HttpResponse
import json as simplejson
from itertools import count


def homepageView(request):
    # user = User.objects.get(username="nfor")
    # notify.send(user, recipient=user, verb='Django notifications',
    #             )
    max = 6
    unread = Notification.objects.filter(
        recipient=request.user, unread=True)[:max]
    unread_no = len(unread)
    read_no = max-unread_no
    read = Notification.objects.filter(
        recipient=request.user, unread=False)[:read_no]
    context = {
        "notify_unread": unread,
        "notify_read": unread
    }
    return render(request, 'app/index.html', context)


def all(request):
    return render(request, 'app/all.html',)


@login_required
def mark_as_read(request, slug=None):
    notification_id = slug2id(slug)

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_read()
    return Response({"result": "success"})


@login_required
def mark_as_unread(request, slug=None):
    notification_id = slug2id(slug)

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_unread()


# This view is currently not being used!
@permission_classes((AllowAny, ))
class get_notifications(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Quizes.
    """

    def list(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


@permission_classes((AllowAny, ))
class mark_read(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Quizes.
    """
    print("Entered")

    def retrieve(self, request, pk=None):
        notification_id = slug2id(pk)
        notification = get_object_or_404(
            Notification, recipient=request.user, id=notification_id)
        notification.mark_as_read()
        return Response({
                        "results": "success",
                        })


@permission_classes((AllowAny, ))
class mark_unread(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Quizes.
    """
    print("Entered")

    def retrieve(self, request, pk=None):
        notification_id = slug2id(pk)
        notification = get_object_or_404(
            Notification, recipient=request.user, id=notification_id)
        notification.mark_as_unread()
        return Response({
                        "results": "success",
                        })


@permission_classes((AllowAny, ))
class mark_all_read(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving Quizes.
    """

    def list(self, request):
        notifications = Notification.objects.filter(recipient=request.user)
        notifications.mark_all_as_read()
        return Response({
                        "results": "success",
                        })


def render_notifications(request):
    max = 6
    if request.is_ajax():
        format = 'json'
        mimetype = 'application/json'
        notifications = Notification.objects.filter(recipient=request.user)
        unread = Notification.objects.filter(
            recipient=request.user, unread=True)[:max]
        unread_no = len(unread)
        read_no = max-unread_no
        read = Notification.objects.filter(
            recipient=request.user, unread=False)[:read_no]
        context = {
            "notify_unread": unread,
            "notify_read": read,
            "notifications": notifications
        }
        #m = str(q['id'])
        #json = simplejson.dumps(message)
        #data = serializers.serialize(format, o)
        # return HttpResponse(data, mimetype)
        unread_count = len(notifications.unread())
        html = render_to_string(
            'app/render.html', context)
        res = {'html': html,
               'unread_count': unread_count
               }
        return HttpResponse(simplejson.dumps(res), mimetype)


def render_all(request):
    if request.is_ajax():
        format = 'json'
        mimetype = 'application/json'
        notifications = Notification.objects.filter(recipient=request.user)
        unread = Notification.objects.filter(
            recipient=request.user, unread=True)
        read = Notification.objects.filter(
            recipient=request.user, unread=False)
        context = {
            "notify_unread": unread,
            "notify_read": read,
            "notifications": notifications
        }
        #m = str(q['id'])
        #json = simplejson.dumps(message)
        #data = serializers.serialize(format, o)
        # return HttpResponse(data, mimetype)
        unread_count = len(notifications.unread())
        html = render_to_string(
            'app/all_render.html', context)
        res = {'html': html,
               'unread_count': unread_count
               }
        return HttpResponse(simplejson.dumps(res), mimetype)
