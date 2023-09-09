from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, TemplateView
from .models import Student, Appointment
from tutor.models import Duration, Tutor, Course
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone
import re
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Appointment, Review


def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return redirect('login')
        if not request.user.user_type:
            return redirect('tutor:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper

# Create your views here.
def create_student(request):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    return redirect('student:profile-create')


def create_student_profile(request):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    curr_user = request.user
    curr_user.user_type = "student"
    curr_user.save()
    new_student = Student()
    first_name = request.POST["first"]
    last_name = request.POST["last"]
    new_student.name = first_name + " " + last_name
    new_student.profile_complete = True
    new_student.save()
    curr_user.student = new_student
    curr_user.save()
    return redirect('student:dashboard')


class StudentDashboardView(UserPassesTestMixin, ListView):
    template_name = 'student/dashboard.html'
    model = Tutor

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'student'

    def handle_no_permission(self):
        return redirect('tutor:dashboard')
    
    def get_context_data(self, **kwargs):
            # if self.request.user.user_type == "tutor":
            #     return redirect("/tutor/dashboard")
            context = super().get_context_data(**kwargs)
            context['q'] = self.request.GET.get('q', '')
            student = self.request.user.student
            pending_appts = Appointment.objects.filter(student=student).filter(approved=None)
            # Add check for datetime for below 2 queries
            past_appts = Appointment.objects.filter(student=student).filter(approved=True).filter(duration__start__lte=timezone.now())
            future_appts = Appointment.objects.filter(student=student).filter(approved=True).filter(duration__start__gt=timezone.now())
            
            q_reviews = []
            for pa in past_appts:
                q_reviews.append(Appointment.objects.get(id=pa.id))
            context["reviews"] = q_reviews
            context["pending_appts"] = pending_appts
            context["pending_len"] = len(pending_appts)
            context["future_appts"] = future_appts
            context["future_len"] = len(future_appts)
            context["past_appts"] = past_appts
            context["past_len"] = len(past_appts)
            return context


def search_view(request):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    student = request.user.student
    q = request.GET.get('query')
    if q:
        course_mnc = re.search(r'[a-zA-Z]{2,5}\s?\d{4}',q)
        if course_mnc != None:
            if(" " in course_mnc.group()):
                course_mnc = course_mnc.group().split(" ")
                subj = course_mnc[0].upper()
                catalog_nbr = course_mnc[1]
            else:
                course_mnc = course_mnc.group()
                subj = course_mnc[:-4].upper()
                catalog_nbr = course_mnc[-4:]
            q_tutors = Tutor.objects.filter(courses__subject__exact=subj).filter(courses__catalog_num__exact=catalog_nbr).distinct()
        else:
            q_tutors = Tutor.objects.filter(Q(courses__title__icontains=q)|Q(courses__subject__iexact=q)|Q(courses__catalog_num__exact=q)|Q(first_name__icontains=q)|Q(last_name__icontains=q)).distinct()
        weekday = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        length = len(q_tutors)
        unavail = []
        for a in Appointment.objects.all():
            if a.student == student and a.approved ==True and a.duration!=None:
                unavail.append(a.duration.start)
        return render(request,'student/search.html',{"results":q_tutors,"weekday":weekday,"length":length,"unavail":unavail})
    return render(request,'student/search.html',{"results":None})
    
    
    #     return JsonResponse({'data': tutor_list})
    # else:
    #     return JsonResponse({'data': 'none'})


def search_page(request):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    return render(request, "student/search.html")


def request_appointment(request,tutor_id):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    print("POST",request.POST)
    new_appt = Appointment()
    # new_appt.time = datetime.now()
    # new_appt.time = request.POST.get("time")
    new_appt.notes = request.POST.get("notes")
    new_appt.tutor = Tutor.objects.get(id=tutor_id)
    new_appt.student = request.user.student
    course_id = request.POST.get("selected-course")
    new_appt.course = Course.objects.get(id=course_id)
    duration_id = request.POST.get("selected-time")
    new_appt.duration = Duration.objects.get(id=duration_id)
    new_appt.time = request.POST.get("selected-time")
    new_appt.save()
    return redirect('student:dashboard')


def tutor_review_view(request, appt_id):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    appt = Appointment.objects.get(id=appt_id)
    return render(request, "student/review.html", {"appt": appt})


def submit_review(request, appt_id):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    new_review = Review()
    print(request.POST)
    rating = int(request.POST.get("star"))
    new_review.rating = rating
    new_review.testimonial = request.POST.get("testimonial")
    appointment = Appointment.objects.get(id=appt_id)
    appointment.reviewed = True
    appointment.save()
    new_review.appointment = appointment
    new_review.save()
    tutor = appointment.tutor
    tutor.average_rating = round(((tutor.average_rating * tutor.number_of_ratings) + rating) / (tutor.number_of_ratings+1),2)
    tutor.number_of_ratings = tutor.number_of_ratings + 1
    tutor.save()
    return redirect('student:dashboard')

def reviews_page(request, tutor_id):
    if request.user.user_type == "tutor":
        return redirect("/tutor/dashboard")
    if not request.user.user_type == "student":
        return redirect("/tutor/dashboard")
    q_tutor = Tutor.objects.get(id=tutor_id)
    q_reviews = Review.objects.filter(appointment__tutor = q_tutor)
    print(q_reviews)
    print(q_tutor)
    return render(request, "student/see-reviews.html", {"tutor":q_tutor,"reviews":q_reviews})
