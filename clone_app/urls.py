from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    #path('login/', views.loginView, name='login'),
    path('create-story/<int:storySet>/', views.createStoryView, name='create-story'),
    path('connectShop/',views.connectShop,name="connectShop"),
    path('storiesList/',views.storiesList,name="storiesList"),
    path('createNewStorySet/',views.createNewStorySet,name="createNewStorySet"),
    path('preview/<int:id>/<int:storySet>/',views.preview,name="preview"),
    path('answers/<int:storySet>/',views.answers,name="answers"),
    path('duplicateStorySet/<int:id>/',views.duplicateStorySet,name="duplicateStorySet"),
    path('removeStorySet/<int:id>/',views.removeStorySet,name="removeStorySet"),
]
