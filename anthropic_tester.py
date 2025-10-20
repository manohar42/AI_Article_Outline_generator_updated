# from typing import List,Optional
# from pydantic import BaseModel, field_validator,ValidationInfo,Field
# from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_anthropic import ChatAnthropic
# from dotenv import load_dotenv
# from src.models.content_models import ContentType, SearchIntent, OutlineSection, ContentGap,FAQ

# load_dotenv()

# # 1) Define schema
# # class ContentBrief(BaseModel):
# #     title: str = Field(description="Concise, specific article title")
# #     primary_keyword: str
# #     sections: List[str] = Field(description="Ordered H2/H3 section titles")
# #     faqs: List[str] = Field(default_factory=list, description="Short FAQ questions")

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




# # 2) Create parser and format instructions
# parser = PydanticOutputParser(pydantic_object=ContentBrief)
# fmt = parser.get_format_instructions()

# # 3) Build prompt with format instructions
# prompt = ChatPromptTemplate.from_template(
#   """ You are an SEO strategist. Create a detailed SEO content brief for the topic "{topic}".
# Return ONLY JSON that matches the exact Pydantic schema.

# If a field in the schema is required, always include it — even if it must be an empty list, string, or 0.

# {format_instructions}"""

# )

# # 4) LLM of choice
# llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0)  # or ChatAnthropic(...)

# # 5) Chain: prompt -> llm -> text -> pydantic
# chain = prompt.partial(format_instructions=fmt) | llm | StrOutputParser() | parser

# # 6) Invoke and receive a validated ContentBrief object
# result: ContentBrief = chain.invoke({"topic": "vector databases for RAG"})
# print(result.model_dump())


from langchain_anthropic import ChatAnthropic
from src.models.content_models import ContentBrief

def _generate_outline_with_llm(context, keywords, content_strategy):
    """Generate structured outline using with_structured_output method"""
    
    system_prompt = """
    You are an expert SEO content strategist.
    Generate a detailed, search-optimized article outline based on the provided context.

    REQUIREMENTS:
    - Create 6-10 main body sections (H2 level)
    - Include Introduction and Conclusion sections
    - Add 3-5 FAQs
    - Ensure word counts sum to total target
    - Use engaging, specific section titles with target keywords
    """
    
    human_template = """Based on the following research context, create a detailed content outline:
    
    {context}
    
    Target primary keyword: {primary_keyword}
    Target word count: {word_count}
    """
    
    # Use Claude with structured output
    llm = ChatAnthropic(
        model="claude-3-5-sonnet-20241022", 
        temperature=0.2
    )
    
    # This is the key change - use with_structured_output
    structured_llm = llm.with_structured_output(ContentBrief)
    
    try:
        result = structured_llm.invoke([
            ("system", system_prompt),
            ("human", human_template.format(
                context=context,
                primary_keyword=keywords.primary if hasattr(keywords, 'primary') else keywords.get('primary', ''),
                word_count=content_strategy.get('estimated_word_count', 2500)
            ))
        ])
        
        print("Structured output result:", result)
        return result
        
    except Exception as e:
        print(f"Error with structured output: {e}")
        return None
