from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from src.models.state_models import OutlineState
from src.models.content_models import ContentBrief, OutlineSection, FAQ, ContentGap
import json
from langchain_anthropic import ChatAnthropic

def generate_content_strategy(state: OutlineState) -> OutlineState:
    """Generate comprehensive content strategy and outline"""
    
    # Extract data from state
    keywords = state['keywords']
    content_strategy = state.get('content_strategy', {})
    competitor_analysis = state.get('competitor_analysis', {})
    serper_results = state.get('serper_results', [])
    content_gaps = state.get('content_gaps', [])
    
    # Build context for LLM
    context = _build_strategy_context(keywords, content_strategy, competitor_analysis, serper_results, content_gaps)
    
    # Generate outline using LLM
    outline = _generate_outline_with_llm(context, keywords, content_strategy)
    
    if outline:
        state['outline'] = outline.dict() if hasattr(outline, 'dict') else outline
        state['confidence_scores']['content_strategy'] = 0.9
    else:
        state['errors'].append("Failed to generate content outline")
        state['confidence_scores']['content_strategy'] = 0.3
    
    return state

def _build_strategy_context(keywords, content_strategy, competitor_analysis, serper_results, content_gaps):
    """Build comprehensive context for strategy generation"""
    
    context_parts = []
    
    # Handle both dict and KeywordData object formats
    if isinstance(keywords, dict):
        primary_keyword = keywords.get('primary', '')
        secondary_keywords = keywords.get('secondary', [])
        lsi_keywords = keywords.get('lsi', [])
        longtail_keywords =None
    else:
        # KeywordData object
        primary_keyword = keywords.primary
        secondary_keywords = keywords.secondary
        lsi_keywords = keywords.lsi
        longtail_keywords = None
    
    # Keywords context
    context_parts.append(f"PRIMARY KEYWORD: {primary_keyword}")
    if secondary_keywords:
        context_parts.append(f"SECONDARY KEYWORDS: {', '.join(secondary_keywords)}")
    if lsi_keywords:
        context_parts.append(f"LSI KEYWORDS: {', '.join(lsi_keywords)}")
    if longtail_keywords:
        context_parts.append(f"LONGTAIL KEYWORDS: {', '.join(longtail_keywords)}")
    
    # Rest of the function remains the same
    context_parts.append(f"CONTENT TYPE: {content_strategy.get('content_type', 'guide')}")
    context_parts.append(f"SEARCH INTENT: {content_strategy.get('search_intent', 'informational')}")
    context_parts.append(f"TARGET WORD COUNT: {content_strategy.get('estimated_word_count', 2500)}")
    
    # Competitor insights
    if competitor_analysis.get('common_topics'):
        context_parts.append(f"COMPETITOR TOPICS: {', '.join(competitor_analysis['common_topics'][:10])}")
    
    # PAA questions
    if serper_results:
        paa_questions = [paa.get('question', '') for paa in serper_results[0].get('people_also_ask', [])][:5]
        if paa_questions:
            context_parts.append(f"PEOPLE ALSO ASK: {'; '.join(paa_questions)}")
    
    # Content gaps
    if content_gaps:
        gap_topics = [gap.get('topic', '') for gap in content_gaps[:3]]
        context_parts.append(f"CONTENT GAPS TO ADDRESS: {'; '.join(gap_topics)}")
    
    return "\n".join(context_parts)


def _generate_outline_with_llm(context, keywords, content_strategy):
    """Generate structured outline using LLM with Pydantic parser"""
    
    parser = PydanticOutputParser(pydantic_object=ContentBrief)
    # fmt = parser.get_format_instructions()
    system_prompt = """
    You are an expert SEO content strategist.
    Your task is to generate a detailed, search-optimized article outline in STRICT JSON adhering to the EXACT schema under OUTPUT FORMAT.

    NON-NEGOTIABLES
    - Return ONLY JSON. No prose, no code fences, no comments.
    - Follow the section order: Introduction → Core Concepts → Applications → Benefits → Challenges → Future Trends → Conclusion → FAQs.
    - Include exactly 4–6 Main Body sections (each an H2).
    - Every section object MUST include ALL fields listed in the schema. If no data, use "" or [] accordingly.
    - For `heading`: use "N/A (Standard intro)" for Introduction and Conclusion; use "Section Title (H2)" for all Main Body sections.
    - `subsections` are H3-level ideas (2–4 per body section).
    - `key_points` must have 3 items; `approach` 2–4 items; `internal_links` 2–4 items; `visual_placement` is one concise line; `transition` is one sentence (empty for the last section).
    - FAQs must be 3–5 items. Each answer is 50–100 words.

    WORD COUNT RULES (CRITICAL VALIDATION)
    - Represent ALL counts as PLAIN INTEGER STRINGS (no commas, no ranges), e.g., "1700", "180".
    - `total_word_count` is a single integer string.
    - Each section’s `suggested_word_count` is a single integer string.
    - The SUM of all section `suggested_word_count` values MUST EQUAL `total_word_count`. If not, adjust evenly across body sections, then Introduction/Conclusion as needed, and re-check before returning.
    - Target distribution (approximate of total):
    • Introduction: 8–10%
    • Body (4–6 sections collectively): 70–80% (split evenly across body sections)
    • Conclusion: 5–8%
    • FAQs: 5–8% (FAQs are NOT included in the sum validation above)

    CONTENT RULES
    - Use actionable, descriptive titles that naturally integrate primary/secondary keywords.
    - Each section adds unique value, avoids filler, and logically progresses through the flow above.
    - Align subsections to practical tasks, frameworks, checklists, examples, metrics, or decision criteria.
    - Use research context to fill gaps and differentiate from competitors.
    - Write brief, specific `research_notes` for every section (3 bullets).

    OUTPUT FORMAT (copy EXACTLY this structure)
    {{
    "title": "string",
    "meta_description": "string (max 155 characters)",
    "content_type": "string",
    "search_intent": "string",
    "target_audience": "string",
    "total_word_count": "string",
    "sections": [
        {{
        "section_id": "string (snake_case)",
        "section_title": "string",
        "heading": "string (e.g., 'Section Title (H2)' or 'N/A (Standard intro)')",
        "short_description": "string (1-2 sentences)",
        "target_keywords": ["string", "string"],
        "suggested_word_count": "string",
        "subsections": ["string", "string"],
        "key_points": ["string", "string", "string"],
        "goal": "string (one sentence)",
        "approach": ["string", "string", "string"],
        "angle": "string (one sentence)",
        "research_notes": ["string", "string", "string"],
        "visual_placement": "string (one line description)",
        "internal_links": ["string", "string", "string"],
        "transition": "string (one sentence, empty for last section)"
        }}
    ],
    "faqs": [
        {{
        "question": "string",
        "answer": "string (50-100 words)",
        "target_keywords": ["string", "string"]
        }}
    ],
    "content_gaps_addressed": [
        {{
        "topic": "string",
        "description": "string",
        "opportunity_score": "integer (1-10)"
        }}
    ],
    "internal_link_opportunities": ["string", "string", "string"]
    }}

    VALIDATION LOGIC (perform before returning)
    1) Choose a `total_word_count` integer string (e.g., "1700").
    2) Allocate counts by the required percentages; split Body evenly across 4–6 sections.
    3) Round to integers and ensure the sum of section counts equals `total_word_count`.
    4) If mismatch occurs, adjust Body sections evenly (+/−1) until exact equality; then return the JSON.

    Return ONLY the JSON described above.
    """

    human_template = """Based on the following research context, create a detailed content outline that adheres EXACTLY to the OUTPUT FORMAT and rules in the system message.

    Context:
    {context}

    Additional Requirements:
    - Craft engaging, specific, keyword-integrated section titles (avoid generic phrasing).
    - Ensure each section targets relevant keywords naturally and adds unique value.
    - Include practical H3-level subsections (2–4 per body section) with actionable detail.
    - Address content gaps from competitor analysis explicitly in `content_gaps_addressed`.
    - Derive FAQs from People Also Ask–style queries relevant to the context (3–5 items, 50–100 word answers).
    - Provide concise, evidence-aware `research_notes` (3 bullets) per section.
    - Use only integer strings for all word counts; validate that summed section counts equal `total_word_count` before returning.

    {format_instructions}
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_template)
    ])


    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    # llm = ChatAnthropic(model="claude-sonnet-4-5", temperature=0.2)


    try:
        chain = prompt | llm | parser
        
        result = chain.invoke({
            "context": context,
            "format_instructions": parser.get_format_instructions()
        })
        
        print("Outline in try block:",result)
        
        return result
        
    except Exception as e:
        print(f"Error Generating result at try:{e}")
        # Fallback: try without parser
        try:
            simple_chain = prompt | llm
            raw_result = simple_chain.invoke({
                "context": context,
                "format_instructions": parser.get_format_instructions()
            })

            print("Outline in Exception block:",raw_result)
            
            # Attempt to parse manually
            return _parse_outline_manually(raw_result.content, keywords, content_strategy)
            
        except Exception as fallback_error:
            return None

def _parse_outline_manually(raw_content, keywords, content_strategy):
    """Fallback manual parsing if Pydantic parser fails"""
    
    # This is a simplified fallback - in production, you'd want more robust parsing
    try:
        # Try to extract JSON from the raw content
        import re
        json_match = re.search(r'\{.*\}', raw_content, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            parsed = json.loads(json_str)
            return parsed
    except:
        pass
    
    # Create minimal fallback outline
    return {
        "title": f"Complete Guide to {keywords.primary.title()}",
        "meta_description": f"Discover everything about {keywords.primary}. Expert insights and recommendations.",
        "content_type": content_strategy.get('content_type', 'ultimate_guide'),
        "search_intent": content_strategy.get('search_intent', 'informational'),
        "target_audience": content_strategy.get('target_audience', 'general audience'),
        "total_word_count": content_strategy.get('estimated_word_count', 2500),
        "sections": [
            {
                "section_id": "introduction",
                "section_title": f"What is {keywords.primary.title()}?",
                "short_description": "Introduction and overview",
                "target_keywords": [keywords.primary],
                "suggested_word_count": 300,
                "subsections": ["Overview", "Key Benefits"],
                "research_notes": ["Define the topic clearly"]
            }
        ],
        "faqs": [],
        "content_gaps_addressed": [],
        "internal_link_opportunities": []
    }



