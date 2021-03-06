from django.db import models
from django.contrib.auth.models import User
from datetime import date
import datetime



class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()


class Entry(models.Model):
    name = models.CharField(max_length=500)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=500)


class choices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    chosen = models.IntegerField(default=0)


class components(models.Model):
    typeChoices = (
        ('image','image'),
        ('text','text'),
        ('emoji','emoji'),
        ('sticker','sticker'),
        ('unsplash','unsplash'),
        ('gif','gif'),
        ('yesNo','yesNo'),
        ('check','check'),
        ('radio','radio'),
        ('timer','timer'),
        ('range','range'),
        ('button','button'),
        ('checkout','checkout'),
        ('dataCollector','dataCollector'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=500, choices=typeChoices)
    title = models.CharField(max_length=500, default="default text for widget", blank=True, null=True)
    href = models.URLField(blank=True, null=True)
    target = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    choices = models.ManyToManyField(choices, blank=True)
    entries = models.ManyToManyField(Entry, blank=True)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    rangeTimes = models.FloatField(blank=True, null=True, default=0)
    rangeCount = models.IntegerField(blank=True, null=True, default=0)
    yesTimes = models.IntegerField(blank=True, null=True, default=0)
    noTimes = models.IntegerField(blank=True, null=True, default=0)
    hours = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    transX = models.CharField(max_length=500, default="-50%")
    transY = models.CharField(max_length=500, default="-50%")
    top = models.CharField(max_length=500, default="50%")
    left = models.CharField(max_length=500, default="50%")
    width = models.CharField(max_length=500, default="220px")
    height = models.CharField(max_length=500, default="auto")
    rotation = models.CharField(max_length=500, default="0deg")
    background = models.CharField(max_length=500, blank=True, null=True, default="white")
    color = models.CharField(max_length=500, blank=True, null=True, default="#333")
    fontSize = models.CharField(max_length=500, blank=True, null=True)
    fontFamily = models.CharField(max_length=500, blank=True, null=True, default="Helvetica")
    textAlign = models.CharField(max_length=500, blank=True, null=True, default="center")


    def choiceSum(self):
        total = 0
        for choice in self.choices.all():
            total += choice.chosen
        return total

    def yesNoCount(self):
        return self.yesTimes + self.noTimes

    def getD1(self):
        f_date = date(int(str(self.date).split('-')[0]), int(str(self.date).split('-')[1]), int(str(self.date).split('-')[2]))
        l_date = date.today()
        l_date = date(int(str(l_date).split('-')[0]), int(str(l_date).split('-')[1]), int(str(l_date).split('-')[2]))
        delta = f_date - l_date
        days = "%02d"%delta.days
        return str(days[0])

    def getD2(self):
        f_date = date(int(str(self.date).split('-')[0]), int(str(self.date).split('-')[1]), int(str(self.date).split('-')[2]))
        l_date = date.today()
        l_date = date(int(str(l_date).split('-')[0]), int(str(l_date).split('-')[1]), int(str(l_date).split('-')[2]))
        delta = f_date - l_date
        days = "%02d"%delta.days
        return str(days[1])

    def getH1(self):
        hours = "%02d"%(int(self.hours) - int(datetime.datetime.now().hour))
        if int(hours) < 0:
            hours = "%02d"%(24 + int(hours))
        return str(hours)[0]


    def getH2(self):
        hours = "%02d"%(int(self.hours) - int(datetime.datetime.now().hour))
        if int(hours) < 0:
            hours = "%02d"%(24 + int(hours))
        return str(hours)[1]

    def getM1(self):
        minutes = "%02d"%(int(self.minutes) - int(datetime.datetime.now().minute))
        if int(minutes) < 0:
            minutes = "%02d"%(60 + int(minutes))
        return str(minutes)[0]

    def getM2(self):
        minutes = "%02d"%(int(self.minutes) - int(datetime.datetime.now().minute))
        if int(minutes) < 0:
            minutes = "%02d"%(60 + int(minutes))
        return str(minutes)[1]



class story(models.Model):
    storyTypeChoices = (
        ("design","design"),
        ("checkout","checkout"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    storyType = models.CharField(max_length=500, choices=storyTypeChoices, default="design")
    date = models.DateTimeField(auto_now_add=True)
    background = models.CharField(max_length=500, default="white")
    components = models.ManyToManyField(components, blank=True)

    def __str__(self):
        return str(self.user)


class storiesSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, blank=True, null=True)
    storiesSet = models.ManyToManyField(story)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    name = models.CharField(max_length=500, default="My Once Story")
    product = models.CharField(max_length=500, null=True, blank=True)
    handle = models.CharField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(max_length=500, null=True, blank=True)
    src = models.TextField(null=True, blank=True)
    views = models.IntegerField(default=0)

    def getFirstStory(self):
        try:
            return self.storiesSet.all()[0]
        except:
            return False

        

