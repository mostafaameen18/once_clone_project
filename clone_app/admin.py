from django.contrib import admin

# Register your models here.

from .models import *



admin.site.register(story)
admin.site.register(components)
admin.site.register(choices)
