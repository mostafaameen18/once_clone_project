from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *
from django.core import files
from io import BytesIO
import requests


def homeView(request):
    return render(request, 'index.html')

def loginView(request):
    return render(request, 'login.html')

def storiesList(request):
    stories = story.objects.filter(user=request.user)
    context = {
        'stories': stories
    }
    return render(request, 'list.html', context)

def duplicateStoryList(request, id):
    original = story.objects.get(id=id)
    copy = story(user=request.user, story=original.story)
    copy.save()
    for image in original.story_images.all():
        copy.story_images.add(image)
    copy.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeStoryList(request, id):
    original = story.objects.get(id=id)
    original.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def createStoryView(request):
    stories = story.objects.filter(user=request.user)
    stories_images = images.objects.filter(user=request.user)
    context = {
        'stories': stories,
        'images': stories_images,
    }
    return render(request, 'story.html', context)


@csrf_exempt
def create_story(request):
    user = request.user
    insert = story(user=user)
    insert.save()
    return HttpResponse(insert.id)

@csrf_exempt
def save_story(request, id):
    user = request.user
    this_story = story.objects.get(user=user, id=id)
    story_data = request.GET['story']
    this_story.story = story_data
    this_story.save()
    return HttpResponse('saved')


@csrf_exempt
def remove_story(request, id):
    user = request.user
    this_story = story.objects.get(user=user, id=id)

    for image in this_story.story_images.all():
        image.delete()
        
    this_story.delete()
    return HttpResponse('removed')

@csrf_exempt
def upload_image(request, id):
    image = request.FILES.get('images')
    insert = images(user=request.user, image=image)
    insert.save()

    image_containing_story = story.objects.get(id=id)
    image_containing_story.story_images.add(insert)
    image_containing_story.save()

    return HttpResponse(insert.image.url)


