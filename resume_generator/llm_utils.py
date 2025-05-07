from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
from config import settings
import json

class ResumeSection(BaseModel):
    """Model for a resume section."""
    title: str = Field(description="The title of the section")
    content: str = Field(description="The content of the section in markdown format")

class ResumeContent(BaseModel):
    """Model for the complete resume content."""
    summary: str = Field(description="Professional summary in markdown format")
    experience: List[ResumeSection] = Field(description="List of experience sections")
    education: List[ResumeSection] = Field(description="List of education sections")
    skills: List[str] = Field(description="List of skills")
    ats_score: float = Field(description="ATS compatibility score (0-100)")

def initialize_llm():
    """Initialize the LLM with Groq."""
    return ChatGroq(
        groq_api_key=settings.GROQ_API_KEY,
        model_name=settings.MODEL_NAME,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS
    )

def format_user_info(user_info: dict) -> str:
    """Format user information for the prompt."""
    formatted = []
    
    # Personal Information
    personal = user_info['personal_info']
    formatted.append("Personal Information:")
    formatted.append(f"Name: {personal['full_name']}")
    formatted.append(f"Title: {personal['title']}")
    formatted.append(f"Location: {personal['location']}")
    formatted.append(f"Email: {personal['email']}")
    formatted.append(f"Phone: {personal['phone']}")
    if personal.get('linkedin'):
        formatted.append(f"LinkedIn: {personal['linkedin']}")
    if personal.get('website'):
        formatted.append(f"Website: {personal['website']}")
    if personal.get('portfolio'):
        formatted.append(f"Portfolio: {personal['portfolio']}")
    formatted.append("")
    
    # Education
    formatted.append("Education:")
    for edu in user_info['education']:
        formatted.append(f"Institution: {edu['institution']}")
        formatted.append(f"Degree: {edu['degree']} in {edu['field']}")
        formatted.append(f"Period: {edu['start_date']} to {edu['end_date']}")
        if edu.get('gpa'):
            formatted.append(f"GPA: {edu['gpa']}")
        if edu.get('coursework'):
            formatted.append(f"Coursework: {edu['coursework']}")
        if edu.get('achievements'):
            formatted.append(f"Achievements: {edu['achievements']}")
        formatted.append("")
    
    # Experience
    formatted.append("Work Experience:")
    for exp in user_info['experience']:
        formatted.append(f"Company: {exp['company']}")
        formatted.append(f"Position: {exp['job_title']}")
        formatted.append(f"Location: {exp['location']}")
        formatted.append(f"Period: {exp['start_date']} to {exp['end_date']}")
        formatted.append("Responsibilities:")
        formatted.append(exp['responsibilities'])
        formatted.append("Achievements:")
        formatted.append(exp['achievements'])
        formatted.append("Tools and Technologies:")
        formatted.append(exp['tools'])
        formatted.append("")
    
    # Skills
    skills = user_info['skills']
    formatted.append("Skills:")
    formatted.append("Technical Skills:")
    formatted.append(skills['technical_skills'])
    formatted.append("\nSoft Skills:")
    formatted.append(skills['soft_skills'])
    formatted.append("\nLanguages:")
    formatted.append(skills['languages'])
    formatted.append("\nCertifications:")
    formatted.append(skills['certifications'])
    
    return "\n".join(formatted)

def create_resume_prompt(job_description: str, user_info: dict) -> ChatPromptTemplate:
    """Create the prompt template for resume generation."""
    formatted_user_info = format_user_info(user_info)
    
    template = """You are an expert resume writer and ATS optimization specialist.
    Create a professional resume in markdown format optimized for the following job description:
    
    {job_description}
    
    Use the following information about the candidate:
    {user_info}
    
    Follow these guidelines:
    1. Format the resume in clean, professional markdown
    2. Optimize content for ATS systems
    3. Highlight relevant achievements and skills
    4. Use strong action verbs
    5. Quantify achievements where possible
    6. Ensure all sections are properly formatted
    
    {format_instructions}
    """
    
    return ChatPromptTemplate.from_template(template)

def generate_resume(job_description: str, user_info: dict) -> ResumeContent:
    """Generate a resume using the LLM."""
    llm = initialize_llm()
    parser = PydanticOutputParser(pydantic_object=ResumeContent)
    
    prompt = create_resume_prompt(
        job_description=job_description,
        user_info=user_info
    )
    
    # Format the prompt with the parser instructions
    formatted_prompt = prompt.format(
        job_description=job_description,
        user_info=format_user_info(user_info),
        format_instructions=parser.get_format_instructions()
    )
    
    # Generate the response
    response = llm.invoke(formatted_prompt)
    
    # Parse the response
    return parser.parse(response.content)

def analyze_job_description(job_description: str) -> dict:
    """Analyze a job description to extract key requirements."""
    llm = initialize_llm()
    
    template = """Analyze the following job description and extract:
    1. Required skills
    2. Preferred qualifications
    3. Key responsibilities
    4. Industry-specific keywords
    
    Job Description:
    {job_description}
    
    Provide the analysis in a structured format.
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    response = llm.invoke(prompt.format(job_description=job_description))
    
    return response.content 