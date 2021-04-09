from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    #path('login/', views.loginView, name='login'),
    path('create-story/<int:storySet>/', views.createStoryView, name='create-story'),
    path('connectShop/',views.connectShop,name="connectShop"),
    path('updateShop/',views.updateShop,name="updateShop"),
    path('storiesList/',views.storiesList,name="storiesList"),
    path('createNewStorySet/',views.createNewStorySet,name="createNewStorySet"),
    path('preview/<str:code>/',views.preview,name="preview"),
    path('answers/<int:storySet>/',views.answers,name="answers"),
    path('duplicateStorySet/<int:id>/',views.duplicateStorySet,name="duplicateStorySet"),
    path('removeStorySet/<int:id>/',views.removeStorySet,name="removeStorySet"),
    path('addEntry/',views.addEntry,name="addEntry"),
    path('downloadEntries/<int:id>/',views.downloadEntries,name="downloadEntries"),
    path("addRadio/<int:componentID>/<int:id>/", views.addRadio, name="addRadio"),
    path("addCheck/<int:id>/", views.addCheck, name="addCheck"),
    path('addYesNoAns/<int:id>/<str:answer>/', views.addYesNoAns,name="addYesNoAns"),
    path("setRange/<int:id>/<int:rv>/", views.setRange, name="setRange"),
]
