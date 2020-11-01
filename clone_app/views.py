from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import *
from accounts.models import customuser
from django.core import files
from io import BytesIO
import requests
import json
from requests.auth import HTTPBasicAuth


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
    try:
        mycustomuser = customuser.objects.get(user=request.user)
        plan = mycustomuser.plan
        if plan == "paid":
            url = "https://{}:{}@{}.myshopify.com/admin/api/2020-10/products.json".format(mycustomuser.shop_api_key, mycustomuser.shop_password, mycustomuser.shop_name)
            res = requests.get(url)
            context['products'] = json.dumps(res.json())
        context['customuser'] = mycustomuser
        context['plan'] = plan
    except:
        pass
    return render(request, 'story.html', context)


def preview(request, id):
    context = {
        'stories': story.objects.filter(user=User.objects.get(id=id))
    }
    return render(request, 'preview.html', context)


def addCheckRadio(request, id):
    mychoice = choices.objects.get(id=id)
    mychoice.chosen  += 1
    mychoice.save()
    return HttpResponse('done')

def removeCheckRadio(request, id):
    mychoice = choices.objects.get(id=id)
    mychoice.chosen -= 1
    mychoice.save()
    return HttpResponse('done')

@csrf_exempt
def setRange(request, id):
    newRangeValue = request.POST.get('newRangeValue')
    rangeValue = request.POST.get('rangeValue')
    mycomponent = components.objects.get(id=id)
    if newRangeValue:
        mycomponent.rangeCount /= rangeValue
        mycomponent.rangeCount *= newRangeValue
    else:
        mycomponent.rangeTimes += 1
        mycomponent.rangeCount *= rangeValue



def answers(request):
    mystories = story.objects.filter(user=request.user)
    context = {
        "stories": mystories
    }
    return render(request, 'answers.html', context)


def connectShop(request):
    user = request.user
    shopName = request.POST.get('shopName')
    shopKey = request.POST.get('shopKey')

    mycustomuser = customuser.objects.get_or_create(user=request.user, shop_name=shopName, shop_api_key=shopKey)
    mycustomuser.plan = "paid"
    mycustomuser.save()

    return redirect('create-story')








@csrf_exempt
def create_story(request):
    user = request.user
    insert = story(user=user)
    insert.save()
    return HttpResponse(insert.id)

@csrf_exempt
def update_story(request, id, bg):
    user = request.user
    this_story = story.objects.get(user=user, id=id)
    this_story.background = bg
    this_story.save()
    return HttpResponse('saved')


@csrf_exempt
def remove_story(request, id):
    user = request.user
    this_story = story.objects.get(user=user, id=id)
    this_story.delete()
    return HttpResponse('removed')

@csrf_exempt
def createComponent(request, id, type):
    user = request.user
    this_story = story.objects.get(id=id)
    try:
        data = request.POST.get('data')
    except:
        pass

    component = components(user=user, type=type)
    if type == "image":
        ourimage = images.objects.get(id=id)
        component.image = ourimage.image
    elif type == "text":
        component.html = data
    elif type == "emoji" or type == "sticker" or type == "unsplash" or type == "gif":
        component.src = data
    elif type == "check":
        component.title = "You can pick multiple choices"
        choice1 = choices(user=user, title="first option")
        choice1.save()
        choice2 = choices(user=user, title="second option")
        choice2.save()
        choice3 = choices(user=user, title="third option")
        choice3.save()
        context = {
            "component_id": component.id,
            "choice_1_id": choice1.id,
            "choice_2_id": choice2.id,
            "choice_3_id": choice3.id,
        }
    elif type == "radio":
        component.title = "You can pick one choice"
        choice1 = choices(user=user, title="first option")
        choice1.save()
        choice2 = choices(user=user, title="second option")
        choice2.save()
        choice3 = choices(user=user, title="third option")
        choice3.save()
        context = {
            "component_id": component.id,
            "choice_1_id": choice1.id,
            "choice_2_id": choice2.id,
            "choice_3_id": choice3.id,
        }
    elif type == "timer":
        component.title = "chrono 24"
        component.hours = 24
        component.minutes = 60
        component.seconds = 60
    elif type == "range":
        component.title = "Evaluate us"
    elif type == "button":
        component.title = "Click Me"

    component.save()
    if type == "check" or type == "radio":
        return HttpResponse(context)

    return HttpResponse(component.id)


@csrf_exempt
def upload_image(request, id):
    image = request.FILES.get('images')
    insert = images(user=request.user, image=image)
    insert.save()

    image_containing_story = story.objects.get(id=id)
    image_containing_story.story_images.add(insert)
    image_containing_story.save()

    return HttpResponse(insert.image.url)


