from django.db import models
from django.contrib.auth.models import User



class images(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()



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
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=500, choices=typeChoices)
    title = models.CharField(max_length=500, default="default text for widget", blank=True, null=True)
    href = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    src = models.TextField(blank=True, null=True)
    html = models.TextField(blank=True, null=True)
    choices = models.ManyToManyField(choices, null=True, blank=True)
    choiceSum = models.IntegerField(blank=True, null=True, default=0)
    clicks = models.IntegerField(blank=True, null=True, default=0)
    rangeTimes = models.FloatField(blank=True, null=True, default=0)
    rangeCount = models.IntegerField(blank=True, null=True, default=0)
    yesTimes = models.IntegerField(blank=True, null=True, default=0)
    noTimes = models.IntegerField(blank=True, null=True, default=0)
    yesNoCount = models.IntegerField(blank=True, null=True, default=0)
    hours = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=True, null=True)
    seconds = models.IntegerField(blank=True, null=True)
    transX = models.CharField(max_length=500, default="-50%")
    transY = models.CharField(max_length=500, default="-50%")
    top = models.CharField(max_length=500, default="50%")
    left = models.CharField(max_length=500, default="50%")
    width = models.CharField(max_length=500, default="220px")
    height = models.CharField(max_length=500, default="auto")
    rotation = models.CharField(max_length=500, default="0deg")
    background = models.CharField(max_length=500, blank=True, null=True, default="white")
    color = models.CharField(max_length=500, blank=True, null=True, default="#333")




class story(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    background = models.CharField(max_length=500, default="white")
    components = models.ManyToManyField(components, null=True, blank=True)

    def __str__(self):
        return str(self.user)

