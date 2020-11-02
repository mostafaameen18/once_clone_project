
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from clone_app.views import *
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static




urlpatterns = [
    path("create_story/", create_story, name="create_story"),
    path("update_story/<int:id>/<str:bg>/", update_story, name="update_story"),
    path("remove_story/<int:id>/", remove_story, name="remove_story"),
    path("createComponent/<int:id>/<str:type>/", createComponent, name="createComponent"),
    path("removeEditableContainer/<str:objId>/", removeEditableContainer, name="removeEditableContainer"),
    path("addChoice/<str:objId>/", addChoice, name="addChoice"),
    path("removeChoice/<str:objId>/", removeChoice, name="removeChoice"),
    path("upload_image/<int:id>/", upload_image, name="upload_image"),
    path("addCheckRadio/<int:id>/", addCheckRadio, name="addCheckRadio"),
    path("removeCheckRadio/<int:id>/", removeCheckRadio, name="removeCheckRadio"),
    path("setRange/<int:id>/", setRange, name="setRange"),
    path('', include('clone_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login-now/', TemplateView.as_view(template_name='google/accounts/login.html'), name='login'),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
