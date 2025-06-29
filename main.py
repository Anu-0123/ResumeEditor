# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import json
import os
from datetime import datetime

app = FastAPI(title="Resume Editor API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for resumes
resumes_db: Dict[str, dict] = {}

class SectionEnhanceRequest(BaseModel):
    section: str
    content: str

class ResumeData(BaseModel):
    data: dict

# Mock AI enhancement function
def mock_ai_enhancement(section: str, content: str) -> str:
    enhancements = {
        "summary": f"Highly accomplished {content} with proven track record",
        "experience": f"Key achievements:\n- Optimized {content}\n- Led teams to success",
        "education": f"Educational Excellence:\n- {content} with honors",
        "skills": f"Technical Proficiencies:\n- Advanced {content}"
    }
    return enhancements.get(section, f"Enhanced {section}: {content}")

@app.post("/ai-enhance")
async def enhance_section(request: SectionEnhanceRequest):
    enhanced_content = mock_ai_enhancement(request.section, request.content)
    return {"enhanced_content": enhanced_content}

@app.post("/save-resume")
async def save_resume(resume: ResumeData):
    resume_id = f"resume_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    resumes_db[resume_id] = resume.data
    return {"message": "Resume saved successfully", "resume_id": resume_id}

@app.get("/get-resume/{resume_id}")
async def get_resume(resume_id: str):
    if resume_id not in resumes_db:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resumes_db[resume_id]

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Mock parsing - in a real app, you'd use a library like pdfminer or python-docx
    mock_parsed_content = {
        "name": "John Doe",
        "summary": "Experienced software developer",
        "experience": [
            {
                "title": "Software Engineer",
                "company": "Tech Corp",
                "duration": "2018-2022",
                "description": "Developed web applications"
            }
        ],
        "education": [
            {
                "degree": "B.S. Computer Science",
                "university": "State University",
                "year": "2018"
            }
        ],
        "skills": ["JavaScript", "Python", "React"]
    }
    
    return mock_parsed_content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)