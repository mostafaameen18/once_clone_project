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
from datetime import datetime
import csv


def homeView(request):
    return render(request, 'index.html')

def loginView(request):
    return render(request, 'login.html')

def storiesList(request):
    if not request.user.is_authenticated:
        return redirect('login')
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
        storySet = storiesSet.objects.get(id=storySet)
        stories_images = images.objects.filter(user=request.user)

        context = {
            'images': stories_images,
            'storySet': storySet,
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
    
    storySet = storiesSet.objects.get(code=code)
    storySet.views += 1
    storySet.save()

    context['storySet'] = storySet
    
    if "ONCE_RADIO_CHOICES" in request.COOKIES:
        context['radio'] = request.COOKIES['ONCE_RADIO_CHOICES']

    if "ONCE_CHECK_CHOICE_ID" in request.COOKIES:
        context['check'] = request.COOKIES['ONCE_CHECK_CHOICE_ID']

    if "ONCE_YES_NO" in request.COOKIES:
        context['yesno'] = request.COOKIES['ONCE_YES_NO']

    if "ONCE_RANGE" in request.COOKIES:
        context['range'] = request.COOKIES['ONCE_RANGE']

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
        driver.find_element_by_xpath('/html/body/div[3]/main/div[1]/div/div/div[2]/div[1]/form/div[2]/div/button').click()
        time.sleep(2)
        driver.get("https://{}/cart".format(mycustomuser.shop_name))
        driver.find_element_by_xpath('//*[@id="updates_large_36877700563110:50daaab6a50d082b93e922a89edee8e2"]').clear()
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


def addRadio(request, componentID, id):
    from . import models

    if "ONCE_RADIO_CHOICES" in request.COOKIES:
        last_choices = request.COOKIES['ONCE_RADIO_CHOICES'].split('|')
        choices_context = {i.split('_')[0]:i.split("_")[1] for i in last_choices}

        if str(componentID) in choices_context:
            if str(choices_context[str(componentID)]) == str(id):
                return HttpResponse('done')
            else:
                mychoice = models.choices.objects.get(id=choices_context[str(componentID)])
                mychoice.chosen -= 1
                mychoice.save()

        choices_context[componentID] = id

        mychoice = models.choices.objects.get(id=id)
        mychoice.chosen  += 1
        mychoice.save()

        newChoiceLine = "|".join(["{}_{}".format(k,choices_context[k]) for k in choices_context])
        res = HttpResponse('done')
        res.set_cookie('ONCE_RADIO_CHOICES',newChoiceLine)
        return res

    else:

        mychoice = models.choices.objects.get(id=id)
        mychoice.chosen  += 1
        mychoice.save()

        res = HttpResponse('done')
        res.set_cookie("ONCE_RADIO_CHOICES", "|".join(["{}_{}".format(componentID, id)]))
        return res

def addCheck(request, id):
    from . import models

    if "ONCE_CHECK_CHOICE_ID" in request.COOKIES:
        
        last_choice = request.COOKIES['ONCE_CHECK_CHOICE_ID'].split('|')

        if str(id) in last_choice:

            mychoice = models.choices.objects.get(id=id)
            mychoice.chosen -= 1
            mychoice.save()

            last_choice.remove(str(id))
            res = HttpResponse('done')
            res.set_cookie('ONCE_CHECK_CHOICE_ID', "|".join(last_choice))
            return res

        else:

            mychoice = models.choices.objects.get(id=id)
            mychoice.chosen  += 1
            mychoice.save()

            last_choice.append(str(id))
            res = HttpResponse('done')
            res.set_cookie('ONCE_CHECK_CHOICE_ID', "|".join(last_choice))
            return res
    else:

        mychoice = models.choices.objects.get(id=id)
        mychoice.chosen  += 1
        mychoice.save()
    
        res = HttpResponse('done')
        res.set_cookie("ONCE_CHECK_CHOICE_ID", "|".join([str(id)]))
        return res


def addYesNoAns(request, id, answer):
    from . import models

    component = components.objects.get(id=id)

    if "ONCE_YES_NO" in request.COOKIES:
        last_choice = request.COOKIES['ONCE_YES_NO'].split('|')
        choices_context = {i.split('_')[0]:i.split("_")[1] for i in last_choice}

        if str(id) in choices_context:
            if str(choices_context[str(id)]) == str(answer):
                return HttpResponse('done')
            else:
                if answer == "yes":
                    component.noTimes -= 1
                    component.yesTimes += 1
                else:
                    component.yesTimes -= 1
                    component.noTimes += 1
                component.save()
                choices_context[str(id)] = str(answer)
        else:
            if answer == "yes":
                component.yesTimes += 1
            else:
                component.noTimes += 1
            component.save()
            choices_context[str(id)] = str(answer)

        newChoiceLine = "|".join(["{}_{}".format(k,choices_context[k]) for k in choices_context])
        res = HttpResponse('done')
        res.set_cookie('ONCE_YES_NO',newChoiceLine)
        return res

    else:
        if answer == "yes":
            component.yesTimes += 1
        else:
            component.noTimes += 1
        component.save()
        res = HttpResponse('done')
        res.set_cookie('ONCE_YES_NO', "|".join(["{}_{}".format(str(id), answer)]))
        return res





@csrf_exempt
def setRange(request, id, rv):
    
    mycomponent = components.objects.get(id=id)

    if "ONCE_RANGE" in request.COOKIES:
        last_choices = request.COOKIES['ONCE_RANGE'].split('|')
        choices_context = {i.split('_')[0]:i.split("_")[1] for i in last_choices}

        if str(id) in choices_context:
            if str(choices_context[str(id)]) == str(rv):
                return HttpResponse('done')
            else:
                mycomponent.rangeTimes -= float(choices_context[str(id)])
                mycomponent.rangeTimes += rv
                mycomponent.save()

        choices_context[id] = rv

        newChoiceLine = "|".join(["{}_{}".format(k,choices_context[k]) for k in choices_context])
        res = HttpResponse('done')
        res.set_cookie('ONCE_RANGE',newChoiceLine)
        return res
    else:
        mycomponent.rangeCount += 1
        mycomponent.rangeTimes += rv
        mycomponent.save()

        res = HttpResponse('done')
        res.set_cookie('ONCE_RANGE',"|".join(["{}_{}".format(id,rv)]))
        return res



@csrf_exempt
def addEntry(request):
    id = request.POST['id']
    name = request.POST['name']
    email = request.POST['email']
    phoneNumber = request.POST['phoneNumber']

    if "ONCE_ENTRY" in request.COOKIES:
        last_entries = request.COOKIES['ONCE_ENTRY'].split('|')
        last_entries_value = request.COOKIES['ONCE_ENTRY_value'].split('|')
        if id in last_entries:
            for value in last_entries_value:
                if id == value.split('_')[0]:
                    entry = Entry.objects.get(id=value.split("_")[1])
                    entry.name = name
                    entry.email = email
                    entry.phoneNumber = phoneNumber
                    entry.save()
                    break
            return HttpResponse('done')
        else:
            entry = Entry(name=name, email=email, phoneNumber=phoneNumber)
            entry.save()

            component = components.objects.get(id=id)
            component.entries.add(entry)

            res = HttpResponse('done')
            res.set_cookie("ONCE_ENTRY", "|".join(last_entries.append(id)))
            res.set_cookie("ONCE_ENTRY_value", "|".join(last_entries_value("{}_{}".format(id,entry.id))))
            return res
    else:

        entry = Entry(name=name, email=email, phoneNumber=phoneNumber)
        entry.save()

        component = components.objects.get(id=id)
        component.entries.add(entry)

        res = HttpResponse('done')
        res.set_cookie("ONCE_ENTRY", "|".join([id]))
        res.set_cookie("ONCE_ENTRY_value", "|".join(["{}_{}".format(id,entry.id)]))
        return res


def downloadEntries(request, id):
    entries = components.objects.get(id=id).entries.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Entries_{}.csv'.format(id)
    writer = csv.writer(response)

    writer.writerow([
        "Name",
        "Email",
        "Phone Number",
    ])
    for entry in entries:
        row = writer.writerow([
            entry.name,
            entry.email,
            entry.phoneNumber,
        ])

    return response






def answers(request, storySet):
    if not request.user.is_authenticated:
        return redirect('login')
    ids = []
    storySet = storiesSet.objects.get(id=storySet)
    totalAnswers = 0
    for i in storySet.storiesSet.all():
        for j in i.components.all():
            if j.type == "range" or j.type == "check" or j.type == "radio" or j.type == "yesNo" or j.type == "dataCollector":
                totalAnswers += 1
    context = {
        "stories": storySet,
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
        component.date = datetime.today().strftime('%Y-%m-%d')
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
    from . import models
    mycomponent = components.objects.get(id=objId)
    choice = models.choices(user=request.user, title="New choice")
    choice.save()
    mycomponent.choices.add(choice)
    mycomponent.save()
    return HttpResponse(choice.id)


def updateChoice(request, id, title):
    from . import models
    choice = models.choices.objects.get(id=id)
    choice.title = title
    choice.save()
    return HttpResponse('done')

def removeChoice(request, objId):
    from . import models
    mychoice = models.choices.objects.get(id=objId)
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


