"""
Prototype pattern examples
"""

import copy


class Resume:
    def __init__(self, name, job_title, skills):
        self.name = name
        self.job_title = job_title
        self.skills = skills

    def clone(self):
        return copy.deepcopy(self)

    def __str__(self):
        return f"Resume of {self.name}\nJob Title: {self.job_title}\nSkills: {', '.join(self.skills)}"


# Original Resume
original_resume = Resume(
    "Sanket Wagh", "Software Engineer", ["Python", "FastAPI", "Docker"]
)

# Clone the resume and modify it for a new job application
new_resume = original_resume.clone()
new_resume.job_title = "Senior Software Engineer"
new_resume.skills.append("AWS")

resume_2 = original_resume.clone()
resume_2.job_title = "Lead Engineer"
resume_2.skills.extend(["Jira", "SQL"])

print("original Resume:\n", original_resume)
print("cloned Resume:\n", new_resume)
print("resume 2:\n", resume_2)
