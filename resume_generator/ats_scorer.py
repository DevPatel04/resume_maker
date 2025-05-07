from typing import List, Dict
import re
from collections import Counter
from config import settings

class ATSScorer:
    def __init__(self):
        self.keyword_weight = settings.KEYWORD_WEIGHT
        self.format_weight = settings.FORMAT_WEIGHT
        self.content_weight = settings.CONTENT_WEIGHT

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text."""
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Split into words and remove common stop words
        words = text.split()
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'of', 'a', 'an'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        return keywords

    def calculate_keyword_match(self, resume_keywords: List[str], job_keywords: List[str]) -> float:
        """Calculate the keyword match score."""
        resume_counter = Counter(resume_keywords)
        job_counter = Counter(job_keywords)
        
        # Calculate intersection of keywords
        common_keywords = set(resume_counter.keys()) & set(job_counter.keys())
        
        if not job_keywords:
            return 0.0
        
        # Calculate match score
        match_score = sum(min(resume_counter[k], job_counter[k]) for k in common_keywords)
        total_keywords = sum(job_counter.values())
        
        return (match_score / total_keywords) * 100

    def check_format_compatibility(self, resume_text: str) -> float:
        """Check resume format compatibility."""
        score = 100.0
        
        # Check for proper section headers
        required_sections = ['experience', 'education', 'skills']
        for section in required_sections:
            if section.lower() not in resume_text.lower():
                score -= 20
        
        # Check for bullet points
        if not re.search(r'[•\-\*]', resume_text):
            score -= 10
        
        # Check for proper spacing
        if re.search(r'\n{3,}', resume_text):
            score -= 10
        
        return max(0, score)

    def evaluate_content_quality(self, resume_text: str) -> float:
        """Evaluate the quality of resume content."""
        score = 100.0
        
        # Check for action verbs
        action_verbs = {'developed', 'created', 'implemented', 'managed', 'led', 'increased', 'improved', 'achieved'}
        if not any(verb in resume_text.lower() for verb in action_verbs):
            score -= 20
        
        # Check for quantified achievements
        if not re.search(r'\d+%|\$\d+|\d+\s*(?:years?|months?|weeks?)', resume_text):
            score -= 20
        
        # Check for proper length
        word_count = len(resume_text.split())
        if word_count < 200:
            score -= 20
        elif word_count > 1000:
            score -= 20
        
        return max(0, score)

    def calculate_ats_score(self, resume_text: str, job_description: str) -> float:
        """Calculate the overall ATS compatibility score."""
        # Extract keywords
        resume_keywords = self.extract_keywords(resume_text)
        job_keywords = self.extract_keywords(job_description)
        
        # Calculate individual scores
        keyword_score = self.calculate_keyword_match(resume_keywords, job_keywords)
        format_score = self.check_format_compatibility(resume_text)
        content_score = self.evaluate_content_quality(resume_text)
        
        # Calculate weighted average
        total_score = (
            keyword_score * self.keyword_weight +
            format_score * self.format_weight +
            content_score * self.content_weight
        )
        
        return round(total_score, 2)

    def get_improvement_suggestions(self, resume_text: str, job_description: str) -> List[str]:
        """Generate suggestions for improving ATS compatibility."""
        suggestions = []
        
        # Extract keywords
        resume_keywords = set(self.extract_keywords(resume_text))
        job_keywords = set(self.extract_keywords(job_description))
        
        # Find missing keywords
        missing_keywords = job_keywords - resume_keywords
        if missing_keywords:
            suggestions.append(f"Add these keywords from the job description: {', '.join(missing_keywords)}")
        
        # Check format
        if not re.search(r'[•\-\*]', resume_text):
            suggestions.append("Use bullet points to improve readability")
        
        # Check for quantified achievements
        if not re.search(r'\d+%|\$\d+|\d+\s*(?:years?|months?|weeks?)', resume_text):
            suggestions.append("Add quantified achievements with numbers and metrics")
        
        # Check for action verbs
        action_verbs = {'developed', 'created', 'implemented', 'managed', 'led', 'increased', 'improved', 'achieved'}
        if not any(verb in resume_text.lower() for verb in action_verbs):
            suggestions.append("Use strong action verbs to begin bullet points")
        
        return suggestions 