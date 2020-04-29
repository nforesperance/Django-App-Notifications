"""notif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import notifications.urls
import app.views as app_views
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'notify', app_views.get_notifications,
                basename='get_notifications')
router.register(r'mark_unread', app_views.mark_unread, basename='mark_unread')
router.register(r'mark_read', app_views.mark_read, basename='mark_read')
router.register(r'mark_all_read', app_views.mark_all_read, basename='mark_all_read')
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^inbox/notifications/',
        include(notifications.urls, namespace='notifications')),
    # Sample app
    path('', app_views.homepageView, name='notifix'),
    url(r'^mark-as-read/(?P<slug>\d+)/$',
        app_views.mark_as_read, name='mark_as_read'),
    url(r'^mark-as-unread/(?P<slug>\d+)/$',
        app_views.mark_as_unread, name='mark_as_unread'),
    url(r'^render_notifications/$',
        app_views.render_notifications, name='render_notifications'),
]

urlpatterns += router.urls
