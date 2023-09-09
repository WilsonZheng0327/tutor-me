from django.contrib import admin
from .models import Student, Appointment, Review

# Register your models here.
admin.site.register(Student)
admin.site.register(Appointment)
admin.site.register(Review)
