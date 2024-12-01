from django.urls import path
from .views import upload_resume
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('upload/', upload_resume, name='upload_resume'),
    path('add-job/', views.add_job, name='add_job'),  # URL to submit a new job
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add-job/', views.job_list, name='add_job'),  # Show job listing
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('add_job/', views.job_management, name='job_management'),  # Make sure this line is correct

]
