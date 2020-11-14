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
import string
from random import *
import time
from . import models

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
    letters = string.ascii_letters
    digits = string.digits
    chars = letters + digits
    min_length = 6
    max_length = 6
    code = "".join(choice(chars) for x in range(randint(min_length, max_length)))

    insert = storiesSet(user=request.user, code=code)
    insert.save()

    if len(customuser.objects.filter(user=request.user)) > 0:
        checkoutStory = story(user=request.user, storyType="checkout", background="dodgerblue")
        checkoutStory.save()
        insert.storiesSet.add(checkoutStory)
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
            'storySet': storySet,
            'entireStorySet': storiesSetIds
        }
        try:
            mycustomuser = customuser.objects.get(user=request.user)
            url = "https://{}:{}@{}/admin/api/2020-10/products.json".format(mycustomuser.shop_api_key, mycustomuser.shop_password, mycustomuser.shop_name)
            res = requests.get(url)
            context['products'] = json.dumps(res.json())
            context['customuser'] = mycustomuser
            context['plan'] = "paid"
        except:
            pass
        return render(request, 'story.html', context)
    except:
        return redirect('storiesList')


@csrf_exempt
def addProductSell(request, storySetId):

    handle = request.POST.get('handle')
    title = request.POST.get('title')
    price = request.POST.get('price')
    src = request.POST.get('src')
    productId = request.POST.get('id')

    storySet = storiesSet.objects.get(id=storySetId)
    storySet.handle = handle
    storySet.title = title
    storySet.price = price
    storySet.src = src
    storySet.product = productId
    storySet.save()
    return HttpResponse('done')


def preview(request, code):
    context = {}
    ids = []
    storiesSetIds = storiesSet.objects.get(code=code)
    for i in storiesSetIds.storiesSet.all():
        ids.append(i.id)
    stories = story.objects.filter(id__in=ids, storyType="design")
    if storiesSetIds.product != None:
        checkoutStory = story.objects.filter(id__in=ids, storyType="checkout")
        context['checkoutStory'] = checkoutStory
    storiesSetIds.views += 1
    storiesSetIds.save()
    context['stories'] = stories
    context['storySet'] = storiesSetIds
    return render(request, 'preview.html', context)

@csrf_exempt
def performCheckout(request):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.support.ui import Select


    quantity = request.POST['quantity']
    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    addressLine1 = request.POST.get('addressLine1')
    addressLine2 = request.POST.get('addressLine2')
    city = request.POST.get('city')
    state = request.POST.get('state')
    country = request.POST.get('country')
    postal = request.POST.get('postal')
    cardNumber = request.POST.get('cardNumber')
    cardHolderName = request.POST.get('cardHolderName')
    expiryDate = request.POST.get('expiryDate')
    securityCode = request.POST.get('securityCode')
    storySetId = request.POST.get('storySet')
    mycustomuser = customuser.objects.get(user=storiesSet.objects.get(id=storySetId).user)
    try:
        url = "https://{}/products/{}/".format(mycustomuser.shop_name, storiesSet.objects.get(id=storySetId).handle)
        options = Options()
        # options.headless = True
        driver = webdriver.Firefox(options=options, executable_path="geckodriver")
        driver.get(url)
        driver.find_element_by_id("password").send_keys('zaffot')
        driver.find_element_by_xpath('/html/body/div/div[2]/div[2]/form/button').click()
        driver.get(url)
        driver.find_element_by_xpath('/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/form/div[2]/div/button').click()
        time.sleep(2)
        driver.get("https://{}/cart".format(mycustomuser.shop_name))
        driver.find_element_by_xpath('//*[@id="updates_large_36877700563110:50daaab6a50d082b93e922a89edee8e2"]').send_keys(quantity)
        driver.find_element_by_xpath('/html/body/div[3]/main/div/div/div[1]/form/div/div/div/div[4]/div[1]/input').click()
        driver.find_element_by_id('checkout_email_or_phone').send_keys(email)
        driver.find_element_by_id('checkout_shipping_address_first_name').send_keys(fname)
        driver.find_element_by_id('checkout_shipping_address_last_name').send_keys(lname)
        driver.find_element_by_id('checkout_shipping_address_address1').send_keys(addressLine1)
        driver.find_element_by_id('checkout_shipping_address_address2').send_keys(addressLine2)
        driver.find_element_by_id('checkout_shipping_address_city').send_keys(city)
        select = Select(driver.find_element_by_id('checkout_shipping_address_country'))
        select.select_by_visible_text(country)
        select = Select(driver.find_element_by_id('checkout_shipping_address_province'))
        select.select_by_visible_text(state)
        driver.find_element_by_id('checkout_shipping_address_zip').send_keys(postal)
        driver.find_element_by_id('continue_button').click()
        driver.find_element_by_id('continue_button').click()
        driver.find_element_by_id('number').send_keys(cardNumber)
        driver.find_element_by_id('name').send_keys(cardHolderName)
        driver.find_element_by_id('expiry').send_keys(expiryDate)
        driver.find_element_by_id('verification_value').send_keys(securityCode)
        driver.find_element_by_id('continue_button').click()
        time.sleep(2)
        driver.quit()
        return HttpResponse('done')
    except:
        return HttpResponse('wrong')


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
def setRange(request, id, rv, nrv):
    rangeValue = int(rv)
    newRangeValue = int(nrv)
    print(newRangeValue)
    print(rangeValue)
    mycomponent = components.objects.get(id=id)
    if rangeValue == 0:
        mycomponent.rangeCount += 1
        mycomponent.rangeTimes += newRangeValue
        mycomponent.save()
    else:
        mycomponent.rangeCount -= 1
        mycomponent.rangeTimes -= rangeValue
        mycomponent.save()
        if newRangeValue != 0:
            mycomponent.rangeCount += 1
            mycomponent.rangeTimes += newRangeValue
            mycomponent.save()

    return HttpResponse('done')



def answers(request, storySet):
    if not request.user.is_authenticated:
        return redirect('login')
    ids = []
    storiesSetIds = storiesSet.objects.get(id=storySet)
    for i in storiesSetIds.storiesSet.all():
        ids.append(i.id)
    mystories = story.objects.filter(user=request.user, id__in=ids)
    totalAnswers = 0
    for i in mystories:
        for j in i.components.all():
            if j.type == "range" or j.type == "check" or j.type == "radio" or j.type == "yesNo":
                totalAnswers += 1
    context = {
        "stories": mystories,
        "totalAnswers": totalAnswers
    }
    return render(request, 'answers.html', context)


def connectShop(request):
    user = request.user
    shopName = request.POST.get('shopName')
    shopKey = request.POST.get('shopKey')
    shopPass = request.POST.get('shopPass')

    try:
        mycustomuser = customuser(user=request.user, shop_name=shopName, shop_api_key=shopKey, shop_password=shopPass)
        mycustomuser.save()

        userStoriesSet = storiesSet.objects.filter(user=request.user)
        for storySet in userStoriesSet:
            checkoutStory = story(user=request.user, storyType="checkout", background="dodgerblue")
            checkoutStory.save()
            storySet.storiesSet.add(checkoutStory)
            storySet.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        return HttpResponse("shop already exists")

def updateShop(request):
    user = request.user
    shopName = request.POST.get('shopName')
    shopKey = request.POST.get('shopKey')
    shopPass = request.POST.get('shopPass')

    mycustomuser = customuser.objects.get(user=request.user)
    mycustomuser.shop_name = shopName
    mycustomuser.shop_api_key = shopKey
    mycustomuser.shop_password = shopPass
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
    if this_story.storyType == "checkout":
        return HttpResponse("checkout")
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
        choice1 = models.choices(user=user, title="first option")
        choice1.save()
        choice2 = models.choices(user=user, title="second option")
        choice2.save()
        choice3 = models.choices(user=user, title="third option")
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
        choice1 = models.choices(user=user, title="first option")
        choice1.save()
        choice2 = models.choices(user=user, title="second option")
        choice2.save()
        choice3 = models.choices(user=user, title="third option")
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
    elif item == "date":
        component.date = data
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
    elif item == "target":
        component.target = data
    elif item == "fontSize":
        component.fontSize = data
    elif item == "fontFamily":
        component.fontFamily = data
    elif item == "textAlign":
        component.textAlign = data


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
def upload_image(request):
    image = request.FILES.get('images')
    insert = images(user=request.user, image=image)
    insert.save()

    context = [{
        "src": insert.image.url,
        "id": insert.id
    }]

    return HttpResponse(json.dumps(context))


