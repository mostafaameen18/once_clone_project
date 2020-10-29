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
        ('yesNo','yesNo'),
        ('check','check'),
        ('radio','radio'),
        ('timer','timer'),
        ('range','range'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=500, choices=typeChoices)
    title = models.CharField(max_length=500, blank=True, null=True)
    href = models.URLField(blank=True, null=True)
    image = models.FileField(null=True, blank=True)
    html = models.TextField(blank=True, null=True)
    choices = models.ManyToManyField(choices, null=True, blank=True)
    rangeTimes = models.FloatField(blank=True, null=True)
    rangeCount = models.IntegerField(blank=True, null=True)
    yesTimes = models.FloatField(blank=True, null=True)
    yesCount = models.IntegerField(blank=True, null=True)
    noTimes = models.FloatField(blank=True, null=True)
    noCount = models.IntegerField(blank=True, null=True)
    transX = models.CharField(max_length=500, default="-50%")
    transY = models.CharField(max_length=500, default="-50%")
    width = models.FloatField()
    height = models.FloatField()
    background = models.CharField(max_length=500, blank=True, null=True)
    color = models.CharField(max_length=500, blank=True, null=True)




class story(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    background = models.CharField(max_length=500)
    components = models.ManyToManyField(components, null=True, blank=True)

    def __str__(self):
        return str(self.user)

