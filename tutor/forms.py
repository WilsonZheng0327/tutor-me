from django import forms
from .models import Availability

class AvailabilityForm(forms.Form):
    day_of_week = forms.ChoiceField(choices=Availability.DAYS_OF_WEEK, required=False)
    hour_of_day = forms.ChoiceField(choices=Availability.HOURS_OF_DAY, required=False)
    available = forms.BooleanField(required=False)