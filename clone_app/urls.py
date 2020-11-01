from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    #path('login/', views.loginView, name='login'),
    path('create-story/', views.createStoryView, name='create-story'),
    path('connectShop/',views.connectShop,name="connectShop"),
    path('storiesList/',views.storiesList,name="storiesList"),
    path('preview/<int:id>/',views.preview,name="preview"),
    path('answers/',views.answers,name="answers"),
    path('duplicateStoryList/<int:id>/',views.duplicateStoryList,name="duplicateStoryList"),
    path('removeStoryList/<int:id>/',views.removeStoryList,name="removeStoryList"),
]
