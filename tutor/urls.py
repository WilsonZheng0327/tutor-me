from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'tutor'

urlpatterns = [
    path('create', views.create_tutor, name="create-tutor"),
    path('dashboard', views.TutorDashboardView.as_view(),name="dashboard"),
    path('profile-create',TemplateView.as_view(template_name='tutor/profile-create.html'),name='profile-create'),
    # path('courses',TemplateView.as_view(template_name="tutor/add_courses.html"),name="add-courses"),
    path('courses',views.course_search, name="course-search"),
    path('add-courses',views.course_search_additional, name="course-search-additional"),
    path('add/<int:course_id>',views.add_course, name="add-course"),
    path('add-more/<int:course_id>',views.add_course_additional, name="add-course-additional"),
    path('remove-courses', views.remove_courses, name='remove-courses'),
    path('remove/<int:course_id>',views.remove_course_action, name="remove-courses-action"),
    path('created', views.create_tutor_profile, name="create-tutor-profile"),
    # path('added', views., name="add-course"),
    path('profile', views.see_bio, name="see-profile"),
    path('edit-bio', views.edit_bio, name="edit-bio"),
    path('save-bio', views.save_bio, name="save-bio"),
    path('approve-appointment/<int:appt_id>', views.approve_appointment, name='approve-appt'),
    # path('done-appointment/<int:appt_id>', views.done_appointment, name='done-appt'),
    path('deny-appointment/<int:appt_id>', views.deny_appointment, name='deny-appt'),
    # path('reviews/<int:tutor_id>',views.tutor_reviews,name='tutor-reviews'),
    path('availability', views.avail, name="availability"),
    # path('availability/update', views.update_availability, name="update-availability"),
    # path('avail',views.avail,name='avail'),
    path('save-availability',views.save_avail,name='save-avail'),
    path('reviews', views.see_reviews, name="reviews"),
]
