from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

class ContentTypeSearchIntent(BaseModel):
    ContentType : str = Field(description="ContentType of the keyword.")
    SearchIntent : str = Field(description="Search Intent of the Article.")
    PriorityScore : str = Field(description="")
class ContentType(str, Enum):
    ULTIMATE_GUIDE = "ultimate_guide"
    HOW_TO = "how_to"
    COMPARISON = "comparison"
    LISTICLE = "listicle"
    REVIEW = "review"

class SearchIntent(str, Enum):
    INFORMATIONAL = "informational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"
    NAVIGATIONAL = "navigational"

class KeywordData(BaseModel):
    primary: str
    secondary: List[str] = []
    lsi: List[str] = []
    longtail: List[str] = []

class ContentGap(BaseModel):
    topic: str
    description: str
    opportunity_score: int = Field(ge=1, le=10)

class OutlineSection(BaseModel):
    section_id: str
    section_title: str
    short_description: str
    target_keywords: List[str]
    suggested_word_count: int = Field(ge=100, le=2000)
    subsections: List[str] = []
    research_notes: List[str] = []

class FAQ(BaseModel):
    question: str
    answer_brief: str
    target_keywords: List[str] = []

# class ContentBrief(BaseModel):
#     title: str
#     meta_description: str
#     content_type: ContentType
#     search_intent: SearchIntent
#     target_audience: str
#     total_word_count: int
#     sections: List[OutlineSection]
#     faqs: List[FAQ]
#     content_gaps_addressed: List[ContentGap]
#     internal_link_opportunities: List[str] = []
    
#     @field_validator('title')
#     @classmethod
#     def title_must_contain_primary_keyword(cls, v, values):
#         if 'target_keywords' in values and values['target_keywords']:
#             primary = values['target_keywords'][0].lower()
#             if primary not in v.lower():
#                 raise ValueError(f"Title should contain primary keyword: {primary}")
#         return v


# class ContentBrief(BaseModel):
#     title: str
#     meta_description: str
#     content_type: ContentType
#     search_intent: SearchIntent
#     target_audience: str
#     total_word_count: int
#     sections: List[OutlineSection]
#     faqs: Optional[List[FAQ]] = Field(default_factory=list)
#     content_gaps_addressed: Optional[List[ContentGap]] = Field(default_factory=list)
#     internal_link_opportunities: List[str] = Field(default_factory=list)


from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

class ContentTypeSearchIntent(BaseModel):
    ContentType: str = Field(description="ContentType of the keyword.")
    SearchIntent: str = Field(description="Search Intent of the Article.")
    PriorityScore: str = Field(description="")

class ContentType(str, Enum):
    ULTIMATE_GUIDE = "ultimate_guide"
    HOW_TO = "how_to"
    COMPARISON = "comparison"
    LISTICLE = "listicle"
    REVIEW = "review"
    INFORMATIONAL = "informational"

class SearchIntent(str, Enum):
    INFORMATIONAL = "informational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"
    NAVIGATIONAL = "navigational"

class KeywordData(BaseModel):
    primary: str
    secondary: List[str] = []
    lsi: List[str] = []
    longtail: List[str] = []

class ContentGap(BaseModel):
    topic: str
    description: str
    opportunity_score: int = Field(ge=1, le=10, default=5)

class OutlineSection(BaseModel):
    """Enhanced section model matching template structure"""
    section_id: str
    section_title: str
    heading: str = Field(description="The actual H2/H3 heading text (e.g., 'Section Title (H2)' or 'N/A (Standard intro)')")
    short_description: str
    target_keywords: List[str] = Field(default_factory=list)
    suggested_word_count: str = Field(description="Word count range like '150-180' or '600-650'")
    subsections: List[str] = Field(default_factory=list, description="H3 subsection titles")
    
    # Template-specific fields for content brief
    key_points: List[str] = Field(default_factory=list, description="3-5 main bullet points to cover")
    goal: str = Field(default="", description="One sentence describing what this section should accomplish")
    approach: List[str] = Field(default_factory=list, description="3-4 bullet points on how to write this section")
    angle: str = Field(default="", description="Unique positioning/perspective for this section")
    research_notes: List[str] = Field(default_factory=list, description="Specific research needed")
    visual_placement: str = Field(default="", description="What visual/graphic goes in this section")
    internal_links: List[str] = Field(default_factory=list, description="Related articles to link to")
    transition: str = Field(default="", description="Transition sentence to next section")

class FAQ(BaseModel):
    question: str
    answer: str = Field(description="Complete answer (not brief)")
    target_keywords: List[str] = Field(default_factory=list)

class ContentBrief(BaseModel):
    title: str
    meta_description: str
    content_type: str = Field(default="Informational")
    search_intent: str = Field(default="Informational")
    target_audience: str
    total_word_count: str = Field(description="Word count range like '1,600-1,800'")
    sections: List[OutlineSection]
    faqs: Optional[List[FAQ]] = Field(default_factory=list)
    content_gaps_addressed: Optional[List[ContentGap]] = Field(default_factory=list)
    internal_link_opportunities: List[str] = Field(default_factory=list)
