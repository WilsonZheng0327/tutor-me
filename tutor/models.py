from django.utils import timezone
from django.db import models
import json
# from login.models import User


# Create your models here.

class Course(models.Model):
   subject = models.CharField(max_length=5)
   catalog_num = models.CharField(max_length=4)
   title = models.CharField(max_length=200)

   def __str__(self) -> str:
      return self.subject + " " + self.catalog_num
   
   class Meta:
    unique_together = ('subject','catalog_num','title',)


# DAYS_OF_WEEK = (
#     (0, 'Monday'),
#     (1, 'Tuesday'),
#     (2, 'Wednesday'),
#     (3, 'Thursday'),
#     (4, 'Friday'),
#     (5, 'Saturday'),
#     (6, 'Sunday'),
# )

DAYS_OF_WEEK = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]

class Duration(models.Model):
   #  day = models.IntegerField(max_length=1,choices=DAYS_OF_WEEK)
    start = models.DateTimeField(null=True)
   #  end = models.DateTimeField(null=True)

    def get_day(self)->str:
       return DAYS_OF_WEEK[self.start.weekday()]
    def get_month(self)->str:
       return MONTHS[self.start.month]
    
    def __str__(self) -> str:
      return self.start.strftime("%I:00 %p, %B %d")

class Tutor(models.Model):
   # user = models.ForeignKey(User, on_delete=models.CASCADE)
   first_name = models.CharField(max_length=200,null=True)
   last_name = models.CharField(max_length=200,null=True)
   courses = models.ManyToManyField(Course)
   rate = models.FloatField(null=True)
   bio = models.TextField(max_length=500,null=True)
   available_times = models.JSONField(null=True, blank=True)
   available_times_next_week = models.JSONField(null=True, blank=True)
   profile_complete = models.BooleanField(null=True)
   average_rating = models.FloatField(default=0)
   number_of_ratings = models.IntegerField(default=0)
   availability = models.ManyToManyField(Duration,null=True)

   def __str__(self):
      return self.first_name + " " + self.last_name
   
   def to_dict(self):
      return {
         'first_name': self.first_name,
         'last_name': self.last_name,
         'courses': self.courses,
         'rate': self.rate,
         'available_times': self.available_times
      }
    
   def set_available_times(self, dict, week):
      if week == 0:
         self.available_times = json.dumps(dict)
      elif week == 1:
         self.available_times_next_week = json.dumps(dict)

   def get_week1_availability(self)->dict:
         if self.available_times == None: return {}
         return json.loads(self.available_times).items()
   def get_week2_availability(self)->dict:
         if self.available_times_next_week == None: return None
         return json.loads(self.available_times_next_week).items()
   
   def get_sorted_avail(self):
      fresh_avail = self.availability.filter(start__gte=timezone.now())
      sorted_avail = sorted(fresh_avail, key=lambda x: x.start)
      return sorted_avail

         
    
class Availability(models.Model):
    DAYS_OF_WEEK = (
        ('Sun', 'Sunday'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
    )

    HOURS_OF_DAY = (
        ('08:00', '8:00 AM'),
        ('09:00', '9:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('13:00', '1:00 PM'),
        ('14:00', '2:00 PM'),
        ('15:00', '3:00 PM'),
        ('16:00', '4:00 PM'),
        ('17:00', '5:00 PM'),
        ('18:00', '6:00 PM'),
        ('19:00', '7:00 PM'),
        ('20:00', '8:00 PM'),
        ('21:00', '9:00 PM'),
    )

    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    hour_of_day = models.CharField(max_length=5, choices=HOURS_OF_DAY)
    available = models.BooleanField(default=False)
