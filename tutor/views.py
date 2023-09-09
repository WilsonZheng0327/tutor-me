from zoneinfo import ZoneInfo

from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Availability, Tutor,Course, Duration
from .forms import AvailabilityForm
import requests
from django.views.generic import ListView
from student.models import Student, Appointment, Review
from django.db.models import Q
import json
from django.http import JsonResponse
import re
from datetime import date, timedelta, datetime, timezone
from django.contrib.auth.mixins import UserPassesTestMixin


def create_tutor(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    return redirect('tutor:profile-create')


def create_tutor_profile(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    curr_user = request.user
    curr_user.user_type = "tutor"
    curr_user.save()
    new_tutor = Tutor()
    new_tutor.first_name = request.POST["first"]
    new_tutor.last_name = request.POST["last"]
    new_tutor.rate = request.POST["rate"]
    new_tutor.bio = request.POST["bio"]
    new_tutor.profile_complete = True
    new_tutor.save()
    curr_user.tutor = new_tutor
    curr_user.save()
    return redirect('tutor:course-search')



##################################################
#######                                    #######
#######              COURSES               #######
#######                                    #######
##################################################


def course_search(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    q = request.GET.get('query')
    if q:
        course_mnc = re.search(r'[a-zA-Z]{2,5}\s\d{4}',q)
        if course_mnc != None:
            course_mnc = course_mnc.group().split(" ")
            subj = course_mnc[0].upper()
            catalog_nbr = course_mnc[1]
            q_courses = Course.objects.filter(subject__exact=subj).filter(catalog_num__exact=catalog_nbr)
        else:
            q_courses = Course.objects.filter(title__contains=q)
            q_courses = Course.objects.filter(Q(title__contains=q)|Q(subject__exact=q.upper())|Q(catalog_num__exact=q))
        q_courses = q_courses.difference(request.user.tutor.courses.all())
        context = {"results": q_courses,
                   "len": len(q_courses)}
        return render(request,'tutor/add_courses.html',context)
    return render(request,'tutor/add_courses.html',{"results":None})

def course_search_additional(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    q = request.GET.get('query')
    if q:
        course_mnc = re.search(r'[a-zA-Z]{2,5}\s\d{4}',q)
        if course_mnc != None:
            course_mnc = course_mnc.group().split(" ")
            subj = course_mnc[0].upper()
            catalog_nbr = course_mnc[1]
            q_courses = Course.objects.filter(subject__exact=subj).filter(catalog_num__exact=catalog_nbr)
        else:
            q_courses = Course.objects.filter(title__contains=q)
            q_courses = Course.objects.filter(Q(title__contains=q)|Q(subject__exact=q.upper())|Q(catalog_num__exact=q))
        q_courses = q_courses.difference(request.user.tutor.courses.all())
        context = {"results": q_courses,
                   "len": len(q_courses)}
        return render(request,'tutor/add_more_courses.html',context)
    return render(request,'tutor/add_more_courses.html',{"results":None})

def add_course(request, course_id):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    tutor.courses.add(Course.objects.get(id=course_id))
    tutor.save()
    return redirect('tutor:course-search')

def add_course_additional(request, course_id):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    tutor.courses.add(Course.objects.get(id=course_id))
    tutor.save()
    return redirect('tutor:course-search-additional')

def get_courses_info(params:dict)->list:
    courses_info=[]
    courses_json = get_courses_json(params)
    for course in courses_json:
        courses_info.append({"subject":course["subject"],"catalog_nbr":course["catalog_nbr"],"descr":course["descr"],"id":course["crse_id"]})
    return courses_info


def get_courses_json(params:dict):
    # common params : subject, term, catalog_nbr
    response = requests.get(create_url(params))
    return response.json()
    

def create_url(params = {"subject":"CS","term":"1232","catalog_nbr":"3140"}):
    BASE_URL = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01"
    url = BASE_URL
    for k,v in params.items():
        url += "&"+k+"="+v
    return url

def remove_course_action(request, course_id):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    tutor.courses.remove(Course.objects.get(id=course_id))
    tutor.save()
    return redirect('tutor:remove-courses')

def remove_courses(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    # tutor.courses.add(Course.objects.get(id=course_id))
    # tutor.save()
    courses = tutor.courses.all()
    context = {"courses": courses}
    return render(request,'tutor/remove-courses.html', context)






##################################################
#######                                    #######
#######            APPOINTMENTS            #######
#######                                    #######
##################################################


def approve_appointment(request, appt_id):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    appt = Appointment.objects.get(id=appt_id)
    appt.approved = True
    # times_dict = json.loads(appt.tutor.available_times)
    # del times_dict[appt.time]
    # print(Appointment.objects.filter(duration__start=appt.duration.start).filter(approved=None))
    Appointment.objects.filter(duration__start=appt.duration.start).filter(approved=None).delete()
    # appt.tutor.available_times = json.dumps(times_dict)
    appt.tutor.save()
    appt.save()


    return redirect('tutor:dashboard')


def deny_appointment(request, appt_id):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    appt = Appointment.objects.get(id=appt_id)
    appt.approved = False
    appt.save()
    return redirect('tutor:dashboard')


### not used anymore
# def done_appointment(request, appt_id):
#     appt = Appointment.objects.get(id=appt_id)
    
#     # appt.past = True
#     appt.save()
#     return redirect('tutor:dashboard')
###


##################################################
#######                                    #######
#######                BIO                 #######
#######                                    #######
##################################################


def see_bio(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    time_slots = {}
    if tutor.available_times:
        time_slots = json.loads(tutor.available_times).items()
    time_slots_next = {}
    if tutor.available_times_next_week:
        time_slots_next = json.loads(tutor.available_times_next_week).items()

    context = {
        "tutor": tutor, 
        "time_slots": time_slots,
        "time_slots_next": time_slots_next,
        "editable": "readonly",
    }
    return render(request, 'tutor/see-profile.html', context)


def edit_bio(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    context = {
        "editable": "",
        "tutor":tutor,
    }
    return render(request, 'tutor/see-profile.html', context)


def save_bio(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    new_first = request.POST.get("edit_first_name")
    print("Got here")
    print("Test: " + str(request.POST.get("testing")))
    if not (new_first is None):
        tutor.first_name = new_first
    else:
        tutor.first_name = tutor.first_name

    new_last = request.POST.get("edit_last_name")
    if not (new_last is None):
        tutor.last_name = new_last
    else:
        tutor.last_name = tutor.last_name

    new_rate = request.POST.get("edit_rate")
    if not (new_rate is None):
        tutor.rate = new_rate
    else:
        tutor.rate = tutor.rate

    new_bio = request.POST.get("edit_bio")
    if not (new_bio is None):
        tutor.bio = new_bio
    else:
        tutor.bio = tutor.bio

    tutor.save()
    return redirect('tutor:see-profile')
    

##################################################
#######                                    #######
#######             DASHBOARD              #######
#######                                    #######
##################################################


class TutorDashboardView(UserPassesTestMixin, ListView):
    template_name = 'tutor/dashboard.html'
    model = Student

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'tutor'

    def handle_no_permission(self):
        return redirect('student:dashboard')
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['q'] = self.request.GET.get('q', '')
            all_appts = []
            for appt in Appointment.objects.all():
                if appt.tutor == self.request.user.tutor:
                    all_appts.append(appt)
            context['all_appts'] = all_appts
            return context
    

##################################################
#######                                    #######
#######            AVAILABILITY            #######
#######                                    #######
##################################################


def avail(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor:Tutor = request.user.tutor
    durations = tutor.availability.all()
    avail_context = []
    print("loaded durs",durations)
    for dur in durations:
        dt = dur.start.replace(tzinfo=ZoneInfo('America/New_York'))
        day_num = dt.day
        month = dt.month
        hour = dt.hour
        print(hour)
        print(day_num,month,hour)
        avail_context.append({"time":int(hour),"day":day_num,"month":month})
    return render(request, 'tutor/new_avail.html',{"avail_context":json.dumps(avail_context)})

def save_avail(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    # need to fix dupes and a bunch of durations being created
    tutor:Tutor = request.user.tutor
    avails = json.loads(request.POST.get('data',''))
    print("json durs",avails)
    tutor.availability.all().delete()
    tutor.save()
    for avail in avails:
        if avail == None: continue
        hour = avail["time"]
        month=avail["month"]
        day=avail["day"]
        dt = datetime(year=datetime.now().year,month=month,hour=hour,day=day)
        dt=dt.replace(tzinfo=ZoneInfo('UTC'))
        dur = Duration(start=dt)
        dur.save()
        tutor.availability.add(dur)
        tutor.save()
    return JsonResponse({"redirect_url":reverse("tutor:see-profile")},status=201)




def see_reviews(request):
    if request.user.user_type == "student":
        return redirect("/student/dashboard")
    tutor = request.user.tutor
    tutor_id = tutor.id
    q_tutor = Tutor.objects.get(id=tutor_id)
    q_reviews = Review.objects.filter(appointment__tutor=q_tutor)
    context = {
        "tutor": tutor,
        "reviews": q_reviews
    }
    return render(request, 'tutor/see-reviews.html', context)

