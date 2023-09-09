from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views


app_name = 'student'

urlpatterns = [
     path('create', views.create_student, name="create-student"),
     path('profile-create',TemplateView.as_view(template_name='student/profile-create.html'),name='profile-create'),
     path('created', views.create_student_profile, name="create-student-profile"),
     path('dashboard',views.StudentDashboardView.as_view(),name="dashboard"),
     path('search', views.search_page, name="search-page"),
     path('search-results', views.search_view, name='search-results'),
     path('request/<int:tutor_id>', views.request_appointment, name='request-appt'),
     path('review/<int:appt_id>', views.tutor_review_view, name='review-tutor'),
     path('submit/<int:appt_id>', views.submit_review, name='submit-review'),
     path('reviews/<int:tutor_id>',views.reviews_page, name="reviews-page"),
     #path('search', views.TutorSearchResultsView.as_view(), name='search-results')
]