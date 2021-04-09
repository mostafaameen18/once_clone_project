
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView
from clone_app.views import *
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from accounts.views import *




urlpatterns = [
    path('addProductSell/<int:storySetId>/', addProductSell, name="addProductSell"),
    path('performCheckout/',performCheckout,name="performCheckout"),
    path("create_story/<int:storySet>/", create_story, name="create_story"),
    path("update_story/<int:id>/<str:bg>/", update_story, name="update_story"),
    path("remove_story/<int:id>/", remove_story, name="remove_story"),
    path("createComponent/<int:id>/<str:type>/", createComponent, name="createComponent"),
    path("updateComponent/<int:id>/<str:item>/", updateComponent, name="updateComponent"),
    path("removeEditableContainer/<str:objId>/", removeEditableContainer, name="removeEditableContainer"),
    path("addChoice/<int:objId>/", addChoice, name="addChoice"),
    path("updateChoice/<int:id>/<str:title>/", updateChoice, name="updateChoice"),
    path("removeChoice/<int:objId>/", removeChoice, name="removeChoice"),
    path("upload_image/", upload_image, name="upload_image"),
    path('', include('clone_app.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('login-now/', TemplateView.as_view(template_name='google/accounts/login.html'), name='login'),
    path('checkAuthEmail/', checkAuthEmail, name="checkAuthEmail"),
    path('verifyLogin/', verifyLogin, name="verifyLogin"),
    path('verifyLoginPro/<str:code>/', verifyLoginPro, name="verifyLoginPro"),
    path('verifyLoginRedirect/<str:code>/', verifyLoginRedirect, name="verifyLoginRedirect"),
    path('resendVerificationEmail/',resendVerificationEmail, name="resendVerificationEmail"),
    path('logout/',signout,name="logout"),
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
