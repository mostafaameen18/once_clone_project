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
from django.http import JsonResponse


def homeView(request):
    return render(request, 'index.html')

def loginView(request):
    return render(request, 'login.html')

def storiesList(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    stories = storiesSet.objects.filter(user=request.user)
    context = {
        'stories': stories
    }
    return render(request, 'list.html', context)

def createNewStorySet(request):
    insert = storiesSet(user=request.user)
    insert.save()
    return redirect("create-story", insert.id)

def duplicateStorySet(request, id):
    original = storiesSet.objects.get(id=id)
    copy = storiesSet(user=request.user)
    copy.save()
    for story in original.storiesSet.all():
        copy.storiesSet.add(story)
    copy.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def removeStorySet(request, id):
    original = storiesSet.objects.get(id=id)
    original.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def createStoryView(request, storySet):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        ids = []
        storiesSetIds = storiesSet.objects.get(id=storySet)
        for i in storiesSetIds.storiesSet.all():
            ids.append(i.id)
        stories = story.objects.filter(user=request.user, id__in=ids)
        stories_images = images.objects.filter(user=request.user)

        context = {
            'stories': stories,
            'images': stories_images,
            'storySet': storySet
        }
        try:
            mycustomuser = customuser.objects.get(user=request.user)
            url = "https://{}:{}@{}.myshopify.com/admin/api/2020-10/products.json".format(mycustomuser.shop_api_key, mycustomuser.shop_password, mycustomuser.shop_name)
            res = requests.get(url)
            context['products'] = json.dumps(res.json())
            context['customuser'] = mycustomuser
            context['plan'] = "paid"
        except:
            pass
        return render(request, 'story.html', context)
    except:
        return redirect('storiesList')


def preview(request, id, storySet):
    ids = []
    storiesSetIds = storiesSet.objects.get(id=storySet)
    for i in storiesSetIds.storiesSet.all():
        ids.append(i.id)
    stories = story.objects.filter(user=User.objects.get(id=id), id__in=ids)
    storiesSetIds.views += 1
    storiesSetIds.save()
    context = {
        'stories': stories
    }
    return render(request, 'preview.html', context)


def addCheckRadio(request, id):
    mychoice = choices.objects.get(id=id)
    mychoice.chosen  += 1
    mychoice.save()
    userComponents = components.objects.filter(user=request.user, type__in=['check','radio'])
    for component in userComponents:
        total = 0
        for choice in component.choices.all():
            total += choice.chosen
        component.choiceSum = total
        component.save()
    return HttpResponse('done')

def removeCheckRadio(request, id):
    mychoice = choices.objects.get(id=id)
    mychoice.chosen -= 1
    mychoice.save()
    userComponents = components.objects.filter(user=request.user, type__in=['check', 'radio'])
    for component in userComponents:
        total = 0
        for choice in component.choices.all():
            total += choice.chosen
        component.choiceSum = total
        component.save()
    return HttpResponse('done')


def addYesNoAns(request, id, answer):
    component = components.objects.get(id=id)
    if answer == "yes":
        component.yesTimes += 1
    if answer == "no":
        component.noTimes += 1
    component.yesNoCount += 1
    component.save()
    return HttpResponse('done')

def removeYesNoAns(request, id, answer):
    component = components.objects.get(id=id)
    if answer == "yes":
        component.yesTimes -= 1
    if answer == "no":
        component.noTimes -= 1
    component.yesNoCount -= 1
    component.save()
    return HttpResponse('done')


@csrf_exempt
def setRange(request, id):
    newRangeValue = request.POST.get('newRangeValue')
    rangeValue = request.POST.get('rangeValue')
    mycomponent = components.objects.get(id=id)
    if int(rangeValue) == 0:
        mycomponent.rangeCount += newRangeValue
        mycomponent.rangeCount *= newRangeValue
    else:
        mycomponent.rangeCount -= rangeValue
        mycomponent.rangeTimes /= rangeValue
        mycomponent.rangeCount += newRangeValue
        mycomponent.rangeTimes *= newRangeValue



def answers(request, storySet):
    if not request.user.is_authenticated:
        return redirect('login')
    ids = []
    storiesSetIds = storiesSet.objects.get(id=storySet)
    for i in storiesSetIds.storiesSet.all():
        ids.append(i.id)
    mystories = story.objects.filter(user=request.user, id__in=ids)
    context = {
        "stories": mystories
    }
    return render(request, 'answers.html', context)


def connectShop(request):
    user = request.user
    shopName = request.POST.get('shopName')
    shopKey = request.POST.get('shopKey')
    shopPass = request.POST.get('shopPass')

    mycustomuser = customuser(user=request.user, shop_name=shopName, shop_api_key=shopKey, shop_password=shopPass)
    mycustomuser.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))








@csrf_exempt
def create_story(request, storySet):
    user = request.user
    insert = story(user=user)
    insert.save()
    myStorySet = storiesSet.objects.get(id=storySet)
    myStorySet.storiesSet.add(insert)
    myStorySet.save()
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
    if this_story.components.all() != None:
        for component in this_story.components.all():
            if component.choices.all() != None:
                for choice in component.choices.all():
                    choice.delete()
            component.delete()
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
        ourimage = images.objects.get(id=data)
        component.image = ourimage.image
    elif type == "text" or type == "block":
        component.html = data
    elif type == "emoji" or type == "sticker" or type == "unsplash" or type == "gif":
        component.src = data
    elif type == "check":
        component.title = "You can pick multiple choices"
        component.save()
        choice1 = choices(user=user, title="first option")
        choice1.save()
        choice2 = choices(user=user, title="second option")
        choice2.save()
        choice3 = choices(user=user, title="third option")
        choice3.save()
        component.choices.add(choice1)
        component.choices.add(choice2)
        component.choices.add(choice3)
        context = {
            "component_id": component.id,
            "choice_1_id": choice1.id,
            "choice_2_id": choice2.id,
            "choice_3_id": choice3.id,
        }
    elif type == "radio":
        component.title = "You can pick one choice"
        component.save()
        choice1 = choices(user=user, title="first option")
        choice1.save()
        choice2 = choices(user=user, title="second option")
        choice2.save()
        choice3 = choices(user=user, title="third option")
        choice3.save()
        component.choices.add(choice1)
        component.choices.add(choice2)
        component.choices.add(choice3)
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
    this_story.components.add(component)
    this_story.save()

    if type == "check" or type == "radio":
        return JsonResponse(context)
    return HttpResponse(component.id)

@csrf_exempt
def updateComponent(request, id, item):
    component = components.objects.get(id=id)
    data = request.POST.get('data')

    if item == "title":
        component.title = data
    elif item == "href":
        component.href = data
    elif item == "html":
        component.html = data
    elif item == "hours":
        component.hours = data
    elif item == "minutes":
        component.minutes = data
    elif item == "seconds":
        component.seconds = data
    elif item == "left":
        component.left = data
    elif item == "top":
        component.top = data
    elif item == "width":
        component.width = data
    elif item == "rotation":
        component.rotation = data
    elif item == "background":
        component.background = data
    elif item == "color":
        component.color = data

    component.save()
    return HttpResponse('done')



def removeEditableContainer(request, objId):
    mycomponent = components.objects.get(id=objId)
    if mycomponent.choices.all() != None:
        for choice in mycomponent.choices.all():
            choice.delete()
    mycomponent.delete()
    return HttpResponse('removed')

def addChoice(request, objId):
    mycomponent = components.objects.get(id=objId)
    choice = choices(user=request.user, title="New choice")
    choice.save()
    mycomponent.choices.add(choice)
    mycomponent.save()
    return HttpResponse(choice.id)


def updateChoice(request, id, title):
    choice = choices.objects.get(id=id)
    choice.title = title
    choice.save()
    return HttpResponse('done')

def removeChoice(request, objId):
    mychoice = choices.objects.get(id=objId)
    mychoice.delete()
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


