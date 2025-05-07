import streamlit as st
from config import settings
from resume_generator import generate_resume, analyze_job_description, ATSScorer, MarkdownFormatter

# Set page configuration
st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state with demo data
if 'personal_info' not in st.session_state:
    st.session_state.personal_info = {
        'full_name': 'John Doe',
        'email': 'john.doe@example.com',
        'phone': '(555) 123-4567',
        'location': 'San Francisco, CA',
        'title': 'Senior Software Engineer',
        'linkedin': 'linkedin.com/in/johndoe',
        'website': 'johndoe.dev',
        'portfolio': 'github.com/johndoe'
    }

if 'education' not in st.session_state:
    st.session_state.education = [{
        'institution': 'Stanford University',
        'degree': 'Master of Science',
        'field': 'Computer Science',
        'start_date': '2018-09-01',
        'end_date': '2020-06-01',
        'gpa': '3.9',
        'coursework': 'Machine Learning, Data Structures, Algorithms',
        'achievements': 'Dean\'s List, Research Assistant'
    }]

if 'experience' not in st.session_state:
    st.session_state.experience = [{
        'company': 'Tech Corp',
        'job_title': 'Senior Software Engineer',
        'start_date': '2020-07-01',
        'end_date': '2023-12-31',
        'location': 'San Francisco, CA',
        'responsibilities': 'Led development of cloud-native applications\nManaged team of 5 engineers\nImplemented CI/CD pipelines',
        'achievements': 'Reduced deployment time by 50%\nIncreased system reliability by 99.9%\nMentored 3 junior developers',
        'tools': 'Python, AWS, Docker, Kubernetes, React'
    }]

if 'skills' not in st.session_state:
    st.session_state.skills = {
        'technical_skills': 'Python\nJavaScript\nReact\nAWS\nDocker\nKubernetes\nCI/CD\nGit',
        'soft_skills': 'Leadership\nCommunication\nProblem Solving\nTeam Management',
        'languages': 'English (Native)\nSpanish (Intermediate)',
        'certifications': 'AWS Certified Solutions Architect\nGoogle Cloud Professional'
    }

if 'job_description' not in st.session_state:
    st.session_state.job_description = {
        'description': '''Senior Software Engineer

We are looking for a Senior Software Engineer to join our team. The ideal candidate will have experience in cloud-native applications and microservices architecture.

Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python and JavaScript
- Experience with cloud platforms (AWS, GCP, or Azure)
- Knowledge of containerization and orchestration (Docker, Kubernetes)
- Experience with CI/CD pipelines
- Strong problem-solving skills
- Excellent communication abilities

Responsibilities:
- Design and implement scalable cloud-native applications
- Lead technical discussions and architecture decisions
- Mentor junior developers
- Collaborate with cross-functional teams
- Implement best practices for code quality and testing
- Optimize application performance and reliability

Nice to have:
- Experience with React and modern frontend frameworks
- Knowledge of machine learning and data processing
- Contributions to open-source projects
- Experience with agile methodologies''',
        'target_position': 'Senior Software Engineer',
        'target_company': 'Tech Innovations Inc',
        'industry': 'Technology'
    }

def main():
    st.title("📝 AI Resume Builder")
    st.markdown("Create an ATS-optimized resume tailored to your target job")
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Choose a section",
            ["Personal Information", "Education", "Experience", "Skills", "Job Description", "Generate Resume"]
        )
    
    # Main content area
    if page == "Personal Information":
        show_personal_info_form()
    elif page == "Education":
        show_education_form()
    elif page == "Experience":
        show_experience_form()
    elif page == "Skills":
        show_skills_form()
    elif page == "Job Description":
        show_job_description_form()
    else:
        show_resume_generation()

def show_personal_info_form():
    st.header("Personal Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Full Name", value=st.session_state.personal_info['full_name'], key="full_name")
        st.text_input("Email", value=st.session_state.personal_info['email'], key="email")
        st.text_input("Phone", value=st.session_state.personal_info['phone'], key="phone")
        st.text_input("Location (City, State, Country)", value=st.session_state.personal_info['location'], key="location")
    
    with col2:
        st.text_input("Professional Title", value=st.session_state.personal_info['title'], key="title")
        st.text_input("LinkedIn URL (optional)", value=st.session_state.personal_info['linkedin'], key="linkedin")
        st.text_input("Personal Website (optional)", value=st.session_state.personal_info['website'], key="website")
        st.text_input("Portfolio Links (optional)", value=st.session_state.personal_info['portfolio'], key="portfolio")

def show_education_form():
    st.header("Education")
    
    # Display existing education entries
    for i, edu in enumerate(st.session_state.education):
        with st.expander(f"Education Entry {i+1}"):
            st.text_input("Institution Name", value=edu['institution'], key=f"institution_{i}")
            st.text_input("Degree Type", value=edu['degree'], key=f"degree_{i}")
            st.text_input("Field of Study", value=edu['field'], key=f"field_{i}")
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Start Date", value=edu['start_date'], key=f"edu_start_{i}")
            with col2:
                st.date_input("End Date", value=edu['end_date'], key=f"edu_end_{i}")
            st.text_input("GPA (optional)", value=edu['gpa'], key=f"gpa_{i}")
            st.text_area("Relevant Coursework (optional)", value=edu['coursework'], key=f"coursework_{i}")
            st.text_area("Academic Achievements (optional)", value=edu['achievements'], key=f"achievements_{i}")
    
    # Add new education entry
    with st.form("education_form"):
        st.text_input("Institution Name", key="new_institution")
        st.text_input("Degree Type", key="new_degree")
        st.text_input("Field of Study", key="new_field")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Start Date", key="new_edu_start")
        with col2:
            st.date_input("End Date", key="new_edu_end")
        st.text_input("GPA (optional)", key="new_gpa")
        st.text_area("Relevant Coursework (optional)", key="new_coursework")
        st.text_area("Academic Achievements (optional)", key="new_achievements")
        
        if st.form_submit_button("Add Education"):
            new_edu = {
                'institution': st.session_state.new_institution,
                'degree': st.session_state.new_degree,
                'field': st.session_state.new_field,
                'start_date': st.session_state.new_edu_start,
                'end_date': st.session_state.new_edu_end,
                'gpa': st.session_state.new_gpa,
                'coursework': st.session_state.new_coursework,
                'achievements': st.session_state.new_achievements
            }
            st.session_state.education.append(new_edu)
            st.success("Education entry added!")

def show_experience_form():
    st.header("Work Experience")
    
    # Display existing experience entries
    for i, exp in enumerate(st.session_state.experience):
        with st.expander(f"Experience Entry {i+1}"):
            st.text_input("Company Name", value=exp['company'], key=f"company_{i}")
            st.text_input("Job Title", value=exp['job_title'], key=f"job_title_{i}")
            col1, col2 = st.columns(2)
            with col1:
                st.date_input("Start Date", value=exp['start_date'], key=f"exp_start_{i}")
            with col2:
                st.date_input("End Date", value=exp['end_date'], key=f"exp_end_{i}")
            st.text_input("Location", value=exp['location'], key=f"job_location_{i}")
            st.text_area("Job Responsibilities", value=exp['responsibilities'], key=f"responsibilities_{i}")
            st.text_area("Key Achievements", value=exp['achievements'], key=f"job_achievements_{i}")
            st.text_area("Tools and Technologies Used", value=exp['tools'], key=f"tools_{i}")
    
    # Add new experience entry
    with st.form("experience_form"):
        st.text_input("Company Name", key="new_company")
        st.text_input("Job Title", key="new_job_title")
        col1, col2 = st.columns(2)
        with col1:
            st.date_input("Start Date", key="new_exp_start")
        with col2:
            st.date_input("End Date", key="new_exp_end")
        st.text_input("Location", key="new_job_location")
        st.text_area("Job Responsibilities", key="new_responsibilities")
        st.text_area("Key Achievements", key="new_job_achievements")
        st.text_area("Tools and Technologies Used", key="new_tools")
        
        if st.form_submit_button("Add Experience"):
            new_exp = {
                'company': st.session_state.new_company,
                'job_title': st.session_state.new_job_title,
                'start_date': st.session_state.new_exp_start,
                'end_date': st.session_state.new_exp_end,
                'location': st.session_state.new_job_location,
                'responsibilities': st.session_state.new_responsibilities,
                'achievements': st.session_state.new_job_achievements,
                'tools': st.session_state.new_tools
            }
            st.session_state.experience.append(new_exp)
            st.success("Experience entry added!")

def show_skills_form():
    st.header("Skills")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_area("Technical Skills (one per line)", value=st.session_state.skills['technical_skills'], key="technical_skills")
        st.text_area("Soft Skills (one per line)", value=st.session_state.skills['soft_skills'], key="soft_skills")
    
    with col2:
        st.text_area("Language Proficiencies (one per line)", value=st.session_state.skills['languages'], key="languages")
        st.text_area("Certifications (one per line)", value=st.session_state.skills['certifications'], key="certifications")

def show_job_description_form():
    st.header("Job Description")
    
    st.text_area("Paste the job description here", value=st.session_state.job_description['description'], height=300, key="job_description")
    st.text_input("Target Position Title", value=st.session_state.job_description['target_position'], key="target_position")
    st.text_input("Company Name (optional)", value=st.session_state.job_description['target_company'], key="target_company")
    st.text_input("Industry (optional)", value=st.session_state.job_description['industry'], key="industry")

def show_resume_generation():
    st.header("Generate Resume")
    
    if st.button("Generate ATS-Optimized Resume"):
        with st.spinner("Generating your resume..."):
            # Prepare user info dictionary
            user_info = {
                'personal_info': st.session_state.personal_info,
                'education': st.session_state.education,
                'experience': st.session_state.experience,
                'skills': st.session_state.skills
            }
            
            # Generate resume
            resume = generate_resume(
                job_description=st.session_state.job_description['description'],
                user_info=user_info
            )
            
            # Calculate ATS score
            ats_scorer = ATSScorer()
            ats_score = ats_scorer.calculate_ats_score(
                resume_text=MarkdownFormatter.format_resume(resume),
                job_description=st.session_state.job_description['description']
            )
            
            # Get improvement suggestions
            suggestions = ats_scorer.get_improvement_suggestions(
                resume_text=MarkdownFormatter.format_resume(resume),
                job_description=st.session_state.job_description['description']
            )
            
            # Display resume preview
            st.markdown("### Resume Preview")
            st.markdown(MarkdownFormatter.format_resume(resume))
            
            # Display ATS analysis
            st.markdown("### ATS Analysis")
            st.markdown(MarkdownFormatter.format_ats_analysis(ats_score, suggestions))
            
            # Add download button
            st.download_button(
                label="Download Resume (Markdown)",
                data=MarkdownFormatter.format_resume(resume),
                file_name="resume.md",
                mime="text/markdown"
            )

if __name__ == "__main__":
    main() 