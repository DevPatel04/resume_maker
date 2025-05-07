from typing import List, Dict
from .llm_utils import ResumeContent, ResumeSection

class MarkdownFormatter:
    @staticmethod
    def format_section(section: ResumeSection) -> str:
        """Format a resume section in markdown."""
        return f"## {section.title}\n\n{section.content}\n\n"

    @staticmethod
    def format_skills(skills: List[str]) -> str:
        """Format skills section in markdown."""
        skills_text = "## Skills\n\n"
        for skill in skills:
            skills_text += f"- {skill}\n"
        return skills_text + "\n"

    @staticmethod
    def format_resume(resume: ResumeContent) -> str:
        """Format the complete resume in markdown."""
        markdown = []
        
        # Add summary
        markdown.append(f"## Professional Summary\n\n{resume.summary}\n\n")
        
        # Add experience sections
        for exp in resume.experience:
            markdown.append(MarkdownFormatter.format_section(exp))
        
        # Add education sections
        for edu in resume.education:
            markdown.append(MarkdownFormatter.format_section(edu))
        
        # Add skills
        markdown.append(MarkdownFormatter.format_skills(resume.skills))
        
        return "".join(markdown)

    @staticmethod
    def format_ats_analysis(ats_score: float, suggestions: List[str]) -> str:
        """Format ATS analysis results in markdown."""
        markdown = ["## ATS Analysis\n\n"]
        
        # Add score
        markdown.append(f"### ATS Compatibility Score: {ats_score}/100\n\n")
        
        # Add suggestions
        if suggestions:
            markdown.append("### Improvement Suggestions\n\n")
            for suggestion in suggestions:
                markdown.append(f"- {suggestion}\n")
        
        return "".join(markdown)

    @staticmethod
    def format_job_analysis(analysis: Dict) -> str:
        """Format job description analysis in markdown."""
        markdown = ["## Job Description Analysis\n\n"]
        
        # Add required skills
        if "required_skills" in analysis:
            markdown.append("### Required Skills\n\n")
            for skill in analysis["required_skills"]:
                markdown.append(f"- {skill}\n")
            markdown.append("\n")
        
        # Add preferred qualifications
        if "preferred_qualifications" in analysis:
            markdown.append("### Preferred Qualifications\n\n")
            for qual in analysis["preferred_qualifications"]:
                markdown.append(f"- {qual}\n")
            markdown.append("\n")
        
        # Add key responsibilities
        if "key_responsibilities" in analysis:
            markdown.append("### Key Responsibilities\n\n")
            for resp in analysis["key_responsibilities"]:
                markdown.append(f"- {resp}\n")
            markdown.append("\n")
        
        # Add industry keywords
        if "industry_keywords" in analysis:
            markdown.append("### Industry Keywords\n\n")
            for keyword in analysis["industry_keywords"]:
                markdown.append(f"- {keyword}\n")
            markdown.append("\n")
        
        return "".join(markdown) 