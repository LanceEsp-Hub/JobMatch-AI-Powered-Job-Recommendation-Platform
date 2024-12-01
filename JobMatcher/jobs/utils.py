import pdfplumber
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



nltk.download('punkt')

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return ' '.join(page.extract_text() for page in pdf.pages)



def suggest_jobs(resume_text, jobs):
    """
    Suggest jobs based on cosine similarity between resume text and job descriptions.

    Args:
        resume_text (str): Extracted text from the resume.
        jobs (QuerySet): List of Job objects from the database.

    Returns:
        list: List of recommended Job objects sorted by similarity.
    """
    # Extract job descriptions and titles
    job_descriptions = [job.description for job in jobs]
    job_titles = [job.title for job in jobs]
    
    # Combine resume text and job descriptions
    texts = [resume_text] + job_descriptions
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Compute the cosine similarity between the resume and job descriptions
    similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    # Sort job recommendations based on similarity score
    recommendations = sorted(
        zip(jobs, similarities[0]), key=lambda x: x[1], reverse=True
    )
    
    # Debug: Print sorted recommendations
    print("Sorted Recommendations (Job, Score):", recommendations)

    # Filter recommendations based on a threshold (e.g., similarity > 0.05)
    threshold = 0.05  # Adjust this threshold as needed
    filtered_recommendations = [job for job, score in recommendations if score > threshold]
    
    # Return the top 3 recommended jobs
    return filtered_recommendations[:3]



# def extract_relevant_text_from_pdf(file_path):
#     with pdfplumber.open(file_path) as pdf:
#         relevant_text = ""
#         for page in pdf.pages:
#             text = page.extract_text()
#             # Extract relevant sections like 'Skills', 'Experience', etc.
#             if "Skills" in text:
#                 relevant_text += text.split("Skills")[1]  # Extract skills section
#             if "Experience" in text:
#                 relevant_text += text.split("Experience")[1]  # Extract experience section
#             if "Summary" in text:
#                 relevant_text += text.split("Summary")[1]  # Extract summary section

#         # Print extracted relevant text to console log
#         print("Relevant Extracted Text:")
#         print(relevant_text)
        
#         return relevant_text


def summarize_text(text, max_length=100):
    # Split the text into words
    words = text.split()
    
    # If there are more words than max_length, truncate to max_length words
    if len(words) > max_length:
        summarized_text = ' '.join(words[:max_length]) + "..."
    else:
        summarized_text = ' '.join(words)
    
    return summarized_text

def extract_relevant_text_from_pdf(file_path):
    relevant_text = ""
    skills_text = ""
    experience_text = ""
    summary_text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # Extract relevant sections
                if "Skills" in text:
                    skills_text = text.split("Skills")[1].split("Experience")[0].strip()  # Extract skills section
                if "Experience" in text:
                    experience_text = text.split("Experience")[1].split("Summary")[0].strip()  # Extract experience section
                if "Summary" in text:
                    summary_text = text.split("Summary")[1].strip()  # Extract summary section

    # Summarize each section based on word count
    summarized_skills = summarize_text(skills_text)
    summarized_experience = summarize_text(experience_text)
    summarized_summary = summarize_text(summary_text)

    # Combine the summarized sections into one relevant text
    relevant_text = f"Skills: {summarized_skills}\nExperience: {summarized_experience}\nSummary: {summarized_summary}"

    # Print the summarized relevant text
    print("Summarized Extracted Text:")
    print(relevant_text)
    
    return relevant_text


# utils.py

def match_jobs_to_resume(job, resume):
    # Here, you can implement your matching logic
    # This example just compares job skills with resume skills (you can extend this)
    
    job_skills = job.skills_required.split(',')  # Assuming skills are stored as a comma-separated string
    resume_skills = resume.skills.split(',')  # Assuming skills are stored in the resume model as a comma-separated string

    # Calculate the match score based on the number of matching skills
    matching_skills = set(job_skills).intersection(set(resume_skills))
    match_score = len(matching_skills) / len(job_skills)  # Simple ratio-based match score

    return match_score

from .models import JobMatch, Resume


from .models import Resume, JobMatch

def calculate_performance_metrics():
    # Total resumes uploaded
    total_resumes = Resume.objects.count()

    # Total job matches (successful or failed)
    total_matches = JobMatch.objects.count()

    # Total successful matches (if score > 0 means success)
    successful_matches = JobMatch.objects.filter(score__gte=0).count()  # Adjust based on your score logic

    # Prepare the metrics
    performance_metrics = {
        'total_resumes': total_resumes,
        'total_matches': total_matches,
        'successful_matches': successful_matches,
    }

    return performance_metrics

def get_top_job_match():
    # Get the job match with the highest score
    top_match = JobMatch.objects.order_by('-score').first()  # Assuming the highest score indicates the best match
    return top_match
