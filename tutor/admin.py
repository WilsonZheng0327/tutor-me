from django.contrib import admin
from .models import Tutor,Course,Duration

# Register your models here.
admin.site.register(Tutor)
admin.site.register(Course)
admin.site.register(Duration)