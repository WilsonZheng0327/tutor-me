from django.db import models
from tutor.models import Tutor, Course, Duration


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name




class Appointment(models.Model):
    time = models.CharField(max_length=500,null=True)
    notes = models.TextField(max_length=500)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    approved = models.BooleanField(default=None, null=True)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, null=True)
    past = models.BooleanField(default=False)
    reviewed = models.BooleanField(default=False)
    duration = models.ForeignKey(Duration,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.tutor) + " tutors " + str(self.student )


class Review(models.Model):
    rating = models.IntegerField(null=False)
    testimonial = models.TextField(null=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING, null=True)






