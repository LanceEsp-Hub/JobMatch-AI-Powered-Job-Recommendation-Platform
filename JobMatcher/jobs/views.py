from django.shortcuts import render
from .forms import ResumeUploadForm
from .models import Job
from .utils import extract_relevant_text_from_pdf, suggest_jobs
from .forms import JobForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate
from .models import Job, JobMatch  # Assuming you have Job and JobMatch models
from django.shortcuts import render
from .models import Job
from .utils import extract_relevant_text_from_pdf, suggest_jobs
from .utils import calculate_performance_metrics, get_top_job_match



def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded resume
            resume = form.save()

            # Extract relevant text from the uploaded resume
            relevant_text = extract_relevant_text_from_pdf(resume.resume_file.path)

            # Get all jobs from the database
            jobs = Job.objects.all()

            # Get job recommendations based on resume content
            recommendations = suggest_jobs(relevant_text, jobs)
            
            # If there are job recommendations, update the status of the resume to 'successful'
            if recommendations:
                resume.status = 'successful'
            else:
                resume.status = 'unsuccessful'  # Set status to 'unsuccessful' if no recommendations

            # Save the updated status
            resume.save()
            
            print("Recommended Jobs:", recommendations)


            # Render the recommendations page with the recommended jobs
            return render(request, 'jobs/recommendations.html', {
                'recommendations': recommendations,                 
                'relevant_text': relevant_text,  # Pass the extracted relevant text

            })
    else:
        form = ResumeUploadForm()

    return render(request, 'jobs/upload_resume.html', {'form': form})


# Decorator to check if the user is an admin
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            # Save the new job
            form.save()
            return redirect('add_job')  # Redirect to the job list page after saving
    else:
        form = JobForm()

    # Retrieve all job match history
    job_matches = JobMatch.objects.all()
    
    jobs = Job.objects.all()  # Fetch all jobs from the database

    print(jobs)  # This will print the list of jobs in the terminal

    # Calculate job performance metrics
    performance_metrics = calculate_performance_metrics()

    # Context for rendering the page
    context = {
        'form': form,
        'job_matches': job_matches,
        'performance_metrics': performance_metrics,
        'jobs': jobs,  # Pass the jobs to the template

    }

    return render(request, 'jobs/add_job.html', context)


def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the 'next' parameter or default to '/add-job/'
            return redirect(request.GET.get('next', '/add-job/'))
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid credentials'})
    return render(request, 'registration/login.html')

def calculate_performance_metrics():
    # Example: Calculate number of job matches, views, etc.
    total_jobs = Job.objects.count()
    total_resumes = Resume.objects.count()  # Correctly fetch count of resumes
    successful_matches = Resume.objects.filter(status='successful').count()  # Count successful matches
    return {
        'total_jobs': total_jobs,
        'total_resumes': total_resumes,  # Add this line
        'successful_matches': successful_matches,
    }
    
from django.shortcuts import render
from .models import JobMatch, Job, Resume

from django.shortcuts import render
from .models import Resume

def job_management(request):
    # Calculate the count of resumes with status 'Successful'
    successful_matches_count = Resume.objects.filter(status='successful').count()

    # Create a dictionary to pass to the template
    performance_metrics = {
        'successful_matches': successful_matches_count,
    }

    # Render the 'add_job.html' template and pass the performance metrics
    return render(request, 'jobs/add_job.html', {'performance_metrics': performance_metrics})


    
def job_list(request):
    # Fetch all jobs from the database
    jobs = Job.objects.all()
    
    print(jobs)  # Ensure this prints QuerySet of jobs


    # Pass jobs to the template
    return render(request, 'jobs/add_job.html', {'jobs': jobs})


from django.shortcuts import get_object_or_404

def delete_job(request, job_id):
    if request.method == 'POST':
        job = get_object_or_404(Job, id=job_id)
        job.delete()
        return redirect('add_job')  # Redirect back to the job list page


def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('add_job')  # Redirect to the job list after saving
    else:
        form = JobForm(instance=job)

    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'jobs/add_job.html', context)

