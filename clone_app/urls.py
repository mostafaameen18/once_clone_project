from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    #path('login/', views.loginView, name='login'),
    path('create-story/', views.createStoryView, name='create-story'),
    path('storiesList/',views.storiesList,name="storiesList"),
    path('duplicateStoryList/<int:id>/',views.duplicateStoryList,name="duplicateStoryList"),
    path('removeStoryList/<int:id>/',views.removeStoryList,name="removeStoryList"),
]
