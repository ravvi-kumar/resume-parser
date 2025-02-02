from pydantic import BaseModel
from typing import Optional, List, Dict

# Model for work field (used in summary)
class WorkField(BaseModel):
    workFieldCode: str
    workFieldDescription: str
    experienceLevelCode: str
    experienceLevelDescription: str

# Model for the highest degree
class HighestDegree(BaseModel):
    localCode: Optional[str] = None
    localDescription: Optional[str] = None
    internationalCode: Optional[str] = None
    internationalDescription: Optional[str] = None
    endDate: Optional[str] = None

# Model for the summary section
class Summary(BaseModel):
    totalExperienceYears: str
    totalExperienceMonths: str
    currentJob: str
    currentEmployer: str
    currentWorkField: WorkField
    highestDegree: HighestDegree
    summaryAmbitionSection: Optional[str] = None
    extraCurricularSection: Optional[str] = None

# Model for the skills section
class LanguageSkill(BaseModel):
    language: str
    level: Optional[str] = None
    code: str

class TechnologySkill(BaseModel):
    name: str
    description: str
    years: str
    last_used: str
    foundIn: str

class Skills(BaseModel):
    languages: List[LanguageSkill]
    technologies: List[TechnologySkill]

# Model for hobbies and profile picture
class Other(BaseModel):
    # hobbies: List[Dict[str, str]]  # List of hobbies as dictionaries
    profilePicture: Optional[Dict] = None

# Model for metadata
class Metadata(BaseModel):
    filename: str
    lang_code: str
    lang: str
    last_modified: str
    partial_extraction_indicator: str

# Model for personal info
class PersonalInfo(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[str] = None
    gender: str

# Model for location info
class Location(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    postcode: Optional[str] = None
    country: str

# Model for contact info
class ContactInfo(BaseModel):
    mobile_number: str
    email: str

# Model for social media links
class SocialMedia(BaseModel):
    linkedin: Optional[str] = None
    github: Optional[str] = None

# Model for experience entries
class Experience(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    position: Optional[str] = None
    company: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    profession: Optional[str] = None
    profession_group: Optional[str] = None
    profession_class: Optional[str] = None
    is_current_experience: Optional[str] = None
    is_latest_experience: Optional[str] = None

# Model for the final response containing all information
class Response(BaseModel):
    personal_info: PersonalInfo
    location: Location
    contact_info: ContactInfo
    social_media: List[SocialMedia]
    experience: List[Experience]
    nationality: Optional[str] = None
    job_title: str
    summary: Summary
    other: Other
    metadata: Metadata
    document_text: Optional[str] = None
    skills: Skills