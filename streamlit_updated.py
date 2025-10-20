# # streamlit.py
# import streamlit as st
# import json
# import time
# from typing import Dict, Any
# import os
# import sys
# from datetime import datetime

# # Add project root to path
# if os.path.exists("src"):
#     sys.path.insert(0, os.getcwd())

# from src.workflows.strategy_graph import (
#     generate_outline_from_topic,
#     generate_outline,
#     process_outline_feedback
# )

# # Page config
# st.set_page_config(
#     page_title="AI Content Strategy Generator",
#     page_icon="📝",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # Custom CSS for professional template-like appearance
# st.markdown("""
# <style>
#     /* Main container */
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 2rem;
#         max-width: 100%;
#     }
    
#     /* Header styling */
#     .strategy-header {
#         font-size: 1.8rem;
#         font-weight: 700;
#         color: #2c3e50;
#         margin-bottom: 1.5rem;
#         padding-bottom: 0.5rem;
#         border-bottom: 3px solid #3498db;
#     }
    
#     /* Section headers */
#     .section-header {
#         font-size: 1.3rem;
#         font-weight: 600;
#         color: #34495e;
#         margin-top: 1.5rem;
#         margin-bottom: 0.8rem;
#         background-color: #ecf0f1;
#         padding: 0.5rem 0.8rem;
#         border-left: 4px solid #3498db;
#     }
    
#     /* Subsection headers */
#     .subsection-header {
#         font-size: 1.1rem;
#         font-weight: 600;
#         color: #2c3e50;
#         margin-top: 1rem;
#         margin-bottom: 0.5rem;
#     }
    
#     /* Content boxes */
#     .content-box {
#         background-color: #f8f9fa;
#         padding: 1rem;
#         border-radius: 0.4rem;
#         margin: 0.5rem 0;
#         border-left: 3px solid #95a5a6;
#     }
    
#     /* Competitor card */
#     .competitor-card {
#         background-color: #fff9e6;
#         padding: 0.8rem;
#         border-radius: 0.4rem;
#         margin: 0.5rem 0;
#         border-left: 3px solid #f39c12;
#     }
    
#     /* FAQ styling */
#     .faq-box {
#         background-color: #e8f4f8;
#         padding: 1rem;
#         border-radius: 0.4rem;
#         margin: 0.8rem 0;
#         border-left: 3px solid #3498db;
#     }
    
#     /* Section detail */
#     .section-detail {
#         background-color: #ffffff;
#         padding: 1rem;
#         border: 1px solid #dee2e6;
#         border-radius: 0.4rem;
#         margin: 0.5rem 0;
#     }
    
#     /* Gap item */
#     .gap-item {
#         background-color: #ffe8f0;
#         padding: 0.6rem;
#         border-radius: 0.3rem;
#         margin: 0.4rem 0;
#         border-left: 3px solid #e91e63;
#         font-size: 0.95rem;
#     }
    
#     /* Input panel */
#     .input-panel {
#         background-color: #f8f9fa;
#         padding: 1.5rem;
#         border-radius: 0.5rem;
#         border: 1px solid #dee2e6;
#     }
    
#     /* Scrollable output */
#     .output-panel {
#         max-height: 85vh;
#         overflow-y: auto;
#         padding-right: 1rem;
#     }
    
#     /* Button styling */
#     .stButton>button {
#         width: 100%;
#         background-color: #3498db;
#         color: white;
#         font-weight: 600;
#         border-radius: 0.4rem;
#         padding: 0.6rem 1rem;
#         border: none;
#     }
    
#     .stButton>button:hover {
#         background-color: #2980b9;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Initialize session state
# def init_session_state():
#     if 'generated_outline' not in st.session_state:
#         st.session_state.generated_outline = None
#     if 'current_state' not in st.session_state:
#         st.session_state.current_state = None
#     if 'generation_history' not in st.session_state:
#         st.session_state.generation_history = []
#     if 'processing' not in st.session_state:
#         st.session_state.processing = False

# init_session_state()

# def format_section_output(section: Dict, section_num: int) -> str:
#     """Format a section following the template structure"""
    
#     title = section.get('section_title', 'Untitled Section')
#     word_count = section.get('suggested_word_count', 'N/A')
    
#     output = f"""
# ### Section {section_num}: {title} ({word_count} words)

# **Heading (H2/H3):** {section.get('heading', title)}  
# **Word Count Target:** {word_count} words

# **Key Points (3-5 bullet points):**
# """
    
#     key_points = section.get('key_points', [])
#     if key_points:
#         for point in key_points:
#             output += f"- {point}\n"
#     else:
#         output += "- Not specified\n"
    
#     output += f"""
# **Goal (1 sentence):**  
# {section.get('goal', 'Not specified')}

# **Approach (3-4 bullet points):**
# """
    
#     approach = section.get('approach', [])
#     if approach:
#         for item in approach:
#             output += f"- {item}\n"
#     else:
#         output += "- Not specified\n"
    
#     output += f"""
# **Angle (1 sentence on unique positioning):**  
# {section.get('angle', 'Not specified')}

# **Research Needed (bullet list):**
# """
    
#     research = section.get('research_notes', [])
#     if research:
#         for note in research:
#             output += f"- {note}\n"
#     else:
#         output += "- Not specified\n"
    
#     output += f"""
# **Visual Placement (one line description):**  
# {section.get('visual_placement', 'Not specified')}

# **Internal Linking Opportunities (list article titles):**
# """
    
#     links = section.get('internal_links', [])
#     if links:
#         for link in links:
#             output += f"- {link}\n"
#     else:
#         output += "- Not specified\n"
    
#     transition = section.get('transition', '')
#     if transition:
#         output += f"""
# **Transition Example (1 sentence):**  
# "{transition}"
# """
    
#     return output

# def display_template_output(result: Dict):
#     """Display output in template format matching the screenshot"""
    
#     st.markdown('<div class="output-panel">', unsafe_allow_html=True)
    
#     # Get data
#     outline = result.get('outline', {})
#     keywords = result.get('keywords', {})
#     competitor_analysis = result.get('competitor_analysis', {})
#     content_gaps = result.get('content_gaps', [])
#     serp_results = result.get('serper_results', [])
    
#     primary_keyword = keywords.get('primary', outline.get('title', 'Topic'))
    
#     # Title
#     st.markdown(f'<div class="strategy-header">{primary_keyword} - Complete Content Strategy</div>', 
#                 unsafe_allow_html=True)
    
#     # ==== 1. COMPETITOR ANALYSIS SUMMARY ====
#     st.markdown('<div class="section-header">1. COMPETITOR ANALYSIS SUMMARY</div>', unsafe_allow_html=True)
    
#     st.markdown('<div class="subsection-header">Top 3-5 Competing Articles</div>', unsafe_allow_html=True)
    
#     # Get organic results from SERP
#     competitors = []
#     if serp_results and len(serp_results) > 0:
#         organic = serp_results[0].get('organic', [])
#         for i, item in enumerate(organic[:5], 1):
#             st.markdown(f"""
# <div class="competitor-card">
# <strong>{i}. {item.get('title', 'Unknown')}</strong><br/>
# <strong>URL:</strong> {item.get('link', 'N/A')}<br/>
# <strong>Snippet:</strong> {item.get('snippet', 'No description')[:150]}...
# </div>
#             """, unsafe_allow_html=True)
#             competitors.append(item)
    
#     if not competitors:
#         st.info("No competitor data available. Run with SERPER_API_KEY for competitor analysis.")
    
#     # Content Depth Analysis
#     st.markdown('<div class="subsection-header">Content Depth Analysis</div>', unsafe_allow_html=True)
    
#     st.markdown("**Common Topics Covered:**")
#     common_topics = competitor_analysis.get('common_topics', [])
#     if common_topics:
#         for topic in common_topics[:8]:
#             st.markdown(f"- {topic}")
#     else:
#         st.markdown("- Basic benefits and drawbacks\n- Health effects\n- Research-backed information")
    
#     # Content Gaps
#     st.markdown('<div class="subsection-header">Content Gaps We Can Fill</div>', unsafe_allow_html=True)
    
#     if content_gaps:
#         for gap in content_gaps[:8]:
#             st.markdown(f"""
# <div class="gap-item">
# <strong>{gap.get('topic', 'Gap Topic')}</strong><br/>
# {gap.get('description', 'No description')}
# </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No specific content gaps identified. Consider unique angles like timing optimization, individual variation, and practical implementation.")
    
#     # ==== 2. SEO ELEMENTS ====
#     st.markdown('<div class="section-header">2. SEO ELEMENTS</div>', unsafe_allow_html=True)
    
#     article_title = outline.get('title', primary_keyword)
#     meta_desc = outline.get('meta_description', '')
    
#     st.markdown(f"""
# **Article Title**  
# {article_title}

# **Meta Title** (60 characters max)  
# {article_title[:60]}

# **Meta Description** (155 characters max)  
# {meta_desc[:155] if meta_desc else f'Discover comprehensive information about {primary_keyword}. Science-backed insights, benefits, and practical guidance.'}

# **Primary Keyword**  
# {primary_keyword}
#     """)
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         st.markdown("**Secondary Keywords (3-5)**")
#         secondary = keywords.get('secondary', [])
#         if secondary:
#             for kw in secondary[:5]:
#                 st.markdown(f"- {kw}")
#         else:
#             st.markdown("- Not analyzed")
    
#     with col2:
#         st.markdown("**LSI Keywords (5-7)**")
#         lsi = keywords.get('lsi', [])
#         if lsi:
#             for kw in lsi[:7]:
#                 st.markdown(f"- {kw}")
#         else:
#             st.markdown("- Not analyzed")
    
#     with col3:
#         st.markdown("**Content Specs**")
#         st.markdown(f"- Word Count: {outline.get('total_word_count', 'N/A')}")
#         st.markdown(f"- Sections: {len(outline.get('sections', []))}")
#         st.markdown(f"- Content Type: {outline.get('content_type', 'Informational')}")
    
#     # ==== 3. ARTICLE STRUCTURE ====
#     st.markdown(f'<div class="section-header">3. ARTICLE STRUCTURE ({outline.get("total_word_count", "1,600-1,800")} words)</div>', 
#                 unsafe_allow_html=True)
    
#     sections = outline.get('sections', [])
    
#     if sections:
#         for i, section in enumerate(sections, 1):
#             with st.expander(f"**Section {i}: {section.get('section_title', 'Untitled')}** ({section.get('suggested_word_count', 'N/A')} words)", 
#                            expanded=False):
#                 st.markdown(format_section_output(section, i))
#     else:
#         st.warning("No sections generated in outline")
    
#     # ==== 4. FAQ SECTION ====
#     st.markdown('<div class="section-header">4. FAQ SECTION</div>', unsafe_allow_html=True)
    
#     st.markdown(f"**FAQ Heading (H2):** Frequently Asked Questions About {primary_keyword}")
    
#     # Generate FAQs from outline or create basic ones
#     faqs = []
    
#     # Check if there are pre-generated FAQs
#     if 'faqs' in outline:
#         faqs = outline.get('faqs', [])
    
#     # If no FAQs, generate basic ones from sections
#     if not faqs and sections:
#         # Generate 5-8 basic FAQs from section content
#         faq_templates = [
#             {"q": f"What are the main benefits of {primary_keyword}?", "section": 0},
#             {"q": f"What are the potential drawbacks of {primary_keyword}?", "section": 1},
#             {"q": f"How does {primary_keyword} affect health?", "section": 0},
#             {"q": f"What is the recommended approach for {primary_keyword}?", "section": 2},
#             {"q": f"What does research say about {primary_keyword}?", "section": 0},
#         ]
        
#         for idx, template in enumerate(faq_templates[:min(5, len(sections))]):
#             section_idx = min(template['section'], len(sections) - 1)
#             section = sections[section_idx]
#             answer = section.get('short_description', '') or \
#                     (section.get('key_points', [''])[0] if section.get('key_points') else 'See detailed information in the article.')
            
#             faqs.append({
#                 'question': template['q'],
#                 'answer': answer
#             })
    
#     if faqs:
#         for i, faq in enumerate(faqs[:8], 1):
#             st.markdown(f"""
# <div class="faq-box">
# <strong>FAQ {i}</strong><br/><br/>
# <strong>Q: {faq.get('question', 'Question not available')}</strong><br/><br/>
# <strong>A:</strong> {faq.get('answer', 'Answer not available')}
# </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No FAQs generated. Add 5-8 questions based on common user searches.")
    
#     # ==== 5. ARTICLE SPECIFICATIONS SUMMARY ====
#     st.markdown('<div class="section-header">5. ARTICLE SPECIFICATIONS SUMMARY</div>', unsafe_allow_html=True)
    
#     st.markdown(f"""
# **Target Word Count:** {outline.get('total_word_count', '1,600-1,800')} words  
# **Content Type:** {outline.get('content_type', 'Informational, evidence-based article')}  
# **Target Audience:** {outline.get('target_audience', 'General audience seeking comprehensive information')}  
# **Reading Level:** 8th-9th grade (accessible but informed)

# **Content Goals:**
# - Establish authority on the topic
# - Drive organic traffic through targeted keywords
# - Provide actionable, research-backed information
# - Encourage engagement and social sharing

# **Visual Requirements:**
# - 1 featured image
# - 3-5 custom infographics or charts
# - Images optimized with alt text containing target keywords

# **Citation Requirements:**
# - Minimum 10-15 credible sources
# - Link to peer-reviewed studies where possible
# - Cite major authoritative organizations
# - Include publication dates for credibility

# **Update Frequency:** Review and update every 6 months with latest research

# **Success Metrics:**
# - Rank top 10 for primary keyword within 90 days
# - Average time on page: 3+ minutes
# - Bounce rate: <65%
# - Social shares: 30+ in first month
#     """)
    
#     st.markdown('</div>', unsafe_allow_html=True)
    
#     # Export options at bottom
#     st.markdown("---")
#     st.markdown("### 📥 Export Options")
    
#     col1, col2, col3 = st.columns(3)
    
#     with col1:
#         json_str = json.dumps(result, indent=2)
#         st.download_button(
#             label="📄 Download JSON",
#             data=json_str,
#             file_name=f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
#             mime="application/json",
#             use_container_width=True
#         )
    
#     with col2:
#         # Create text summary
#         text_output = f"# {primary_keyword} - Content Strategy\n\n"
#         text_output += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
#         text_output += f"## Article Outline\n\n"
#         text_output += f"Title: {article_title}\n"
#         text_output += f"Word Count: {outline.get('total_word_count', 'N/A')}\n\n"
        
#         for i, section in enumerate(sections, 1):
#             text_output += f"\n### {i}. {section.get('section_title', 'Untitled')}\n"
#             text_output += f"Word Count: {section.get('suggested_word_count', 'N/A')}\n"
#             text_output += f"Description: {section.get('short_description', 'N/A')}\n"
        
#         st.download_button(
#             label="📝 Download Text",
#             data=text_output,
#             file_name=f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
#             mime="text/plain",
#             use_container_width=True
#         )
    
#     with col3:
#         if st.button("🔄 Generate New Strategy", use_container_width=True):
#             st.session_state.current_state = None
#             st.session_state.generated_outline = None
#             st.rerun()

# def main():
#     # App title
#     st.title("🚀 AI Content Strategy Generator")
#     st.markdown("*Generate comprehensive, template-based content strategies*")
#     st.markdown("---")
    
#     # Check API keys
#     openai_key = os.getenv("OPENAI_API_KEY")
#     serper_key = os.getenv("SERPER_API_KEY")
    
#     if not openai_key:
#         st.error("⚠️ OPENAI_API_KEY not found! Please set it in your .env file or environment variables.")
#         st.stop()
    
#     if not serper_key:
#         st.warning("⚠️ SERPER_API_KEY not found. Competitor analysis will be limited.")
    
#     # Two-column layout: Input on left, Output on right
#     col_input, col_output = st.columns([1, 2])
    
#     with col_input:
#         st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        
#         st.markdown("### 📋 Input Configuration")
        
#         # Mode selection
#         mode = st.radio(
#             "Generation Mode",
#             ["Topic-based (with research)", "Keywords-based (no research)"],
#             help="Topic-based performs full keyword research and competitor analysis"
#         )
        
#         st.markdown("---")
        
#         # Input fields based on mode
#         if mode == "Topic-based (with research)":
#             st.markdown("#### 🔍 Enter Topic")
#             topic = st.text_input(
#                 "Topic",
#                 placeholder="e.g., Coffee positives and negatives",
#                 help="Enter the main topic for content strategy",
#                 key="topic_input"
#             )
#             keywords_data = None
            
#         else:
#             st.markdown("#### 🔑 Enter Keywords")
            
#             primary_kw = st.text_input(
#                 "Primary Keyword",
#                 placeholder="e.g., coffee positives and negatives",
#                 help="Main target keyword"
#             )
            
#             secondary_kw = st.text_area(
#                 "Secondary Keywords (one per line)",
#                 placeholder="coffee benefits\\ncoffee side effects\\ncoffee health",
#                 height=100
#             )
            
#             lsi_kw = st.text_area(
#                 "LSI Keywords (one per line)",
#                 placeholder="caffeine effects\\ncoffee research\\ncoffee consumption",
#                 height=100
#             )
            
#             keywords_data = {
#                 'primary': primary_kw.strip(),
#                 'secondary': [kw.strip() for kw in secondary_kw.split('\n') if kw.strip()],
#                 'lsi': [kw.strip() for kw in lsi_kw.split('\n') if kw.strip()]
#             }
            
#             topic = primary_kw
        
#         st.markdown("---")
        
#         # Settings
#         st.markdown("#### ⚙️ Content Settings")
        
#         word_count = st.slider(
#             "Target Word Count",
#             min_value=1000,
#             max_value=5000,
#             value=1800,
#             step=100
#         )
        
#         tone = st.selectbox(
#             "Tone",
#             ["Professional", "Academic", "Casual", "Conversational"]
#         )
        
#         audience = st.selectbox(
#             "Target Audience",
#             ["General audience", "Professionals", "Students", "Health-conscious adults", "Experts"]
#         )
        
#         user_preferences = {
#             "tone": tone.lower(),
#             "target_audience": audience.lower()
#         }
        
#         st.markdown("---")
        
#         # Generate button
#         generate_clicked = st.button(
#             "🚀 Generate Strategy",
#             type="primary",
#             disabled=st.session_state.processing,
#             use_container_width=True
#         )
        
#         # Feedback section if outline exists
#         if st.session_state.current_state:
#             st.markdown("---")
#             st.markdown("#### 💬 Refine Strategy")
            
#             feedback = st.text_area(
#                 "Feedback",
#                 placeholder="e.g., Add more about health benefits, make it more technical",
#                 height=100
#             )
            
#             if st.button("🔄 Apply Feedback", disabled=st.session_state.processing, use_container_width=True):
#                 if feedback.strip():
#                     st.session_state.processing = True
                    
#                     try:
#                         with st.spinner("Processing feedback..."):
#                             updated_state = process_outline_feedback(
#                                 st.session_state.current_state,
#                                 feedback.strip()
#                             )
                            
#                             st.session_state.current_state = updated_state
#                             st.session_state.generated_outline = updated_state.get('outline')
                            
#                             st.success("✅ Feedback applied!")
#                             time.sleep(1)
#                             st.rerun()
                    
#                     except Exception as e:
#                         st.error(f"Error: {str(e)}")
                    
#                     finally:
#                         st.session_state.processing = False
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     with col_output:
#         if generate_clicked:
#             if not topic or not topic.strip():
#                 st.error("Please enter a topic or primary keyword")
#             else:
#                 st.session_state.processing = True
                
#                 try:
#                     with st.status("Generating content strategy...", expanded=True) as status:
#                         st.write("🔍 Step 1: Analyzing keywords...")
                        
#                         # Generate based on mode
#                         if mode == "Topic-based (with research)":
#                             st.write("🌐 Step 2: Researching competitors...")
#                             st.write("🎯 Step 3: Analyzing content gaps...")
#                             st.write("📝 Step 4: Creating outline...")
                            
#                             result = generate_outline_from_topic(
#                                 topic=topic.strip(),
#                                 word_count=word_count,
#                                 user_preferences=user_preferences
#                             )
#                         else:
#                             st.write("📝 Step 2: Creating outline...")
                            
#                             result = generate_outline(
#                                 keywords_data=keywords_data,
#                                 word_count=word_count,
#                                 user_preferences=user_preferences
#                             )
                        
#                         st.session_state.current_state = result
#                         st.session_state.generated_outline = result.get('outline')
                        
#                         # Add to history
#                         st.session_state.generation_history.append({
#                             'timestamp': datetime.now().isoformat(),
#                             'mode': mode,
#                             'input': topic,
#                             'result': result
#                         })
                        
#                         st.write("✅ Strategy generated successfully!")
#                         status.update(label="✅ Generation complete!", state="complete")
                        
#                         time.sleep(1)
#                         st.rerun()
                
#                 except Exception as e:
#                     st.error(f"❌ Generation failed: {str(e)}")
#                     st.exception(e)
                
#                 finally:
#                     st.session_state.processing = False
        
#         # Display output if available
#         if st.session_state.current_state:
#             display_template_output(st.session_state.current_state)
#         else:
#             st.info("👈 Enter a topic and click 'Generate Strategy' to begin")
            
#             # Show example
#             st.markdown("### 📖 Example Output")
#             st.markdown("""
# This tool will generate a comprehensive content strategy including:

# 1. **Competitor Analysis** - Top competing articles with strengths/weaknesses
# 2. **SEO Elements** - Optimized titles, meta descriptions, and keywords
# 3. **Article Structure** - Detailed sections with word counts, key points, and transitions
# 4. **FAQ Section** - 5-8 frequently asked questions with answers
# 5. **Specifications** - Content goals, visual requirements, and success metrics

# The output follows professional content strategy templates used by top content marketing teams.
#             """)

# if __name__ == "__main__":
#     main()

# streamlit.py
import streamlit as st
import json
import time
from typing import Dict, Any
import os
import sys
from datetime import datetime

# Add project root to path
if os.path.exists("src"):
    sys.path.insert(0, os.getcwd())

from src.workflows.strategy_graph import (
    generate_outline_from_topic,
    generate_outline,
    process_outline_feedback
)

# Page config
st.set_page_config(
    page_title="AI Content Strategy Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional template-like appearance
st.markdown("""
<style>
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .strategy-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3498db;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #34495e;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        background-color: #ecf0f1;
        padding: 0.5rem 0.8rem;
        border-left: 4px solid #3498db;
    }
    
    /* Subsection headers */
    .subsection-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Article section header */
    .article-section-header {
        font-size: 1.15rem;
        font-weight: 700;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        padding: 0.6rem 0.8rem;
        background-color: #f8f9fa;
        border-left: 4px solid #27ae60;
    }
    
    /* Content boxes */
    .content-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.4rem;
        margin: 0.5rem 0;
        border-left: 3px solid #95a5a6;
    }
    
    /* Competitor card */
    .competitor-card {
        background-color: #fff9e6;
        padding: 0.8rem;
        border-radius: 0.4rem;
        margin: 0.5rem 0;
        border-left: 3px solid #f39c12;
    }
    
    /* FAQ styling */
    .faq-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.4rem;
        margin: 0.8rem 0;
        border-left: 3px solid #3498db;
    }
    
    /* Section detail box */
    .section-detail {
        background-color: #ffffff;
        padding: 1.2rem;
        border: 1px solid #dee2e6;
        border-radius: 0.4rem;
        margin: 0.8rem 0;
    }
    
    /* Gap item */
    .gap-item {
        background-color: #ffe8f0;
        padding: 0.6rem;
        border-radius: 0.3rem;
        margin: 0.4rem 0;
        border-left: 3px solid #e91e63;
        font-size: 0.95rem;
    }
    
    /* Input panel */
    .input-panel {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
    }
    
    /* Scrollable output */
    .output-panel {
        max-height: 85vh;
        overflow-y: auto;
        padding-right: 1rem;
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background-color: #3498db;
        color: white;
        font-weight: 600;
        border-radius: 0.4rem;
        padding: 0.6rem 1rem;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
    }
    
    /* Section divider */
    .section-divider {
        border-top: 2px solid #dee2e6;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'generated_outline' not in st.session_state:
        st.session_state.generated_outline = None
    if 'current_state' not in st.session_state:
        st.session_state.current_state = None
    if 'generation_history' not in st.session_state:
        st.session_state.generation_history = []
    if 'processing' not in st.session_state:
        st.session_state.processing = False

init_session_state()

def display_article_section(section: Dict, section_num: int):
    """Display a single article section in normal text format with proper headings"""
    
    title = section.get('section_title', 'Untitled Section')
    word_count = section.get('suggested_word_count', 'N/A')
    
    # Section header
    st.markdown(f'<div class="article-section-header">Section {section_num}: {title} ({word_count} words)</div>', 
                unsafe_allow_html=True)
    
    st.markdown('<div class="section-detail">', unsafe_allow_html=True)
    
    # Heading
    heading = section.get('heading', title)
    st.markdown(f"**Heading (H2/H3):** {heading}")
    
    # Word count target
    st.markdown(f"**Word Count Target:** {word_count} words")
    
    st.markdown("")  # spacing
    
    # Key Points
    st.markdown("**Key Points (3-5 bullet points):**")
    key_points = section.get('key_points', [])
    if key_points:
        for point in key_points:
            st.markdown(f"- {point}")
    else:
        st.markdown("- Not specified")
    
    st.markdown("")  # spacing
    
    # Goal
    goal = section.get('goal', 'Not specified')
    st.markdown(f"**Goal (1 sentence):**  \n{goal}")
    
    st.markdown("")  # spacing
    
    # Approach
    st.markdown("**Approach (3-4 bullet points):**")
    approach = section.get('approach', [])
    if approach:
        for item in approach:
            st.markdown(f"- {item}")
    else:
        st.markdown("- Not specified")
    
    st.markdown("")  # spacing
    
    # Angle
    angle = section.get('angle', 'Not specified')
    st.markdown(f"**Angle (1 sentence on unique positioning):**  \n{angle}")
    
    st.markdown("")  # spacing
    
    # Research Needed
    st.markdown("**Research Needed (bullet list):**")
    research = section.get('research_notes', [])
    if research:
        for note in research:
            st.markdown(f"- {note}")
    else:
        st.markdown("- Not specified")
    
    st.markdown("")  # spacing
    
    # Visual Placement
    visual = section.get('visual_placement', 'Not specified')
    st.markdown(f"**Visual Placement (one line description):**  \n{visual}")
    
    st.markdown("")  # spacing
    
    # Internal Linking Opportunities
    st.markdown("**Internal Linking Opportunities (list article titles):**")
    links = section.get('internal_links', [])
    if links:
        for link in links:
            st.markdown(f"- {link}")
    else:
        st.markdown("- Not specified")
    
    st.markdown("")  # spacing
    
    # Transition Example
    transition = section.get('transition', '')
    if transition:
        st.markdown(f"**Transition Example (1 sentence):**  \n*\"{transition}\"*")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Divider between sections
    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

def display_template_output(result: Dict):
    """Display output in template format matching the screenshot"""
    
    st.markdown('<div class="output-panel">', unsafe_allow_html=True)
    
    # Get data
    outline = result.get('outline', {})
    keywords = result.get('keywords', {})
    competitor_analysis = result.get('competitor_analysis', {})
    content_gaps = result.get('content_gaps', [])
    serp_results = result.get('serper_results', [])
    
    primary_keyword = keywords.get('primary', outline.get('title', 'Topic'))
    
    # Title
    st.markdown(f'<div class="strategy-header">{primary_keyword} - Complete Content Strategy</div>', 
                unsafe_allow_html=True)
    
    # ==== 1. COMPETITOR ANALYSIS SUMMARY ====
    st.markdown('<div class="section-header">1. COMPETITOR ANALYSIS SUMMARY</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="subsection-header">Top 3-5 Competing Articles</div>', unsafe_allow_html=True)
    
    # Get organic results from SERP
    competitors = []
    if serp_results and len(serp_results) > 0:
        organic = serp_results[0].get('organic', [])
        for i, item in enumerate(organic[:5], 1):
            st.markdown(f"""
<div class="competitor-card">
<strong>{i}. {item.get('title', 'Unknown')}</strong><br/>
<strong>URL:</strong> {item.get('link', 'N/A')}<br/>
<strong>Snippet:</strong> {item.get('snippet', 'No description')[:150]}...
</div>
            """, unsafe_allow_html=True)
            competitors.append(item)
    
    if not competitors:
        st.info("No competitor data available. Run with SERPER_API_KEY for competitor analysis.")
    
    # Content Depth Analysis
    st.markdown('<div class="subsection-header">Content Depth Analysis</div>', unsafe_allow_html=True)
    
    st.markdown("**Common Topics Covered:**")
    common_topics = competitor_analysis.get('common_topics', [])
    if common_topics:
        for topic in common_topics[:8]:
            st.markdown(f"- {topic}")
    else:
        st.markdown("- Basic benefits and drawbacks\n- Health effects\n- Research-backed information")
    
    # Content Gaps
    st.markdown('<div class="subsection-header">Content Gaps We Can Fill</div>', unsafe_allow_html=True)
    
    if content_gaps:
        for gap in content_gaps[:8]:
            st.markdown(f"""
<div class="gap-item">
<strong>{gap.get('topic', 'Gap Topic')}</strong><br/>
{gap.get('description', 'No description')}
</div>
            """, unsafe_allow_html=True)
    else:
        st.info("No specific content gaps identified. Consider unique angles like timing optimization, individual variation, and practical implementation.")
    
    # ==== 2. SEO ELEMENTS ====
    st.markdown('<div class="section-header">2. SEO ELEMENTS</div>', unsafe_allow_html=True)
    
    article_title = outline.get('title', primary_keyword)
    meta_desc = outline.get('meta_description', '')
    
    st.markdown(f"""
**Article Title**  
{article_title}

**Meta Title** (60 characters max)  
{article_title[:60]}

**Meta Description** (155 characters max)  
{meta_desc[:155] if meta_desc else f'Discover comprehensive information about {primary_keyword}. Science-backed insights, benefits, and practical guidance.'}

**Primary Keyword**  
{primary_keyword}
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Secondary Keywords (3-5)**")
        secondary = keywords.get('secondary', [])
        if secondary:
            for kw in secondary[:5]:
                st.markdown(f"- {kw}")
        else:
            st.markdown("- Not analyzed")
    
    with col2:
        st.markdown("**LSI Keywords (5-7)**")
        lsi = keywords.get('lsi', [])
        if lsi:
            for kw in lsi[:7]:
                st.markdown(f"- {kw}")
        else:
            st.markdown("- Not analyzed")
    
    with col3:
        st.markdown("**Content Specs**")
        st.markdown(f"- Word Count: {outline.get('total_word_count', 'N/A')}")
        st.markdown(f"- Sections: {len(outline.get('sections', []))}")
        st.markdown(f"- Content Type: {outline.get('content_type', 'Informational')}")
    
    # ==== 3. ARTICLE STRUCTURE ====
    st.markdown(f'<div class="section-header">3. ARTICLE STRUCTURE ({outline.get("total_word_count", "1,600-1,800")} words)</div>', 
                unsafe_allow_html=True)
    
    sections = outline.get('sections', [])
    
    if sections:
        for i, section in enumerate(sections, 1):
            display_article_section(section, i)
    else:
        st.warning("No sections generated in outline")
    
    # ==== 4. FAQ SECTION ====
    st.markdown('<div class="section-header">4. FAQ SECTION</div>', unsafe_allow_html=True)
    
    st.markdown(f"**FAQ Heading (H2):** Frequently Asked Questions About {primary_keyword}")
    
    # Generate FAQs from outline or create basic ones
    faqs = []
    
    # Check if there are pre-generated FAQs
    if 'faqs' in outline:
        faqs = outline.get('faqs', [])
    
    # If no FAQs, generate basic ones from sections
    if not faqs and sections:
        # Generate 5-8 basic FAQs from section content
        faq_templates = [
            {"q": f"What are the main benefits of {primary_keyword}?", "section": 0},
            {"q": f"What are the potential drawbacks of {primary_keyword}?", "section": 1},
            {"q": f"How does {primary_keyword} affect health?", "section": 0},
            {"q": f"What is the recommended approach for {primary_keyword}?", "section": 2},
            {"q": f"What does research say about {primary_keyword}?", "section": 0},
        ]
        
        for idx, template in enumerate(faq_templates[:min(5, len(sections))]):
            section_idx = min(template['section'], len(sections) - 1)
            section = sections[section_idx]
            answer = section.get('short_description', '') or \
                    (section.get('key_points', [''])[0] if section.get('key_points') else 'See detailed information in the article.')
            
            faqs.append({
                'question': template['q'],
                'answer': answer
            })
    
    if faqs:
        for i, faq in enumerate(faqs[:8], 1):
            st.markdown(f"""
<div class="faq-box">
<strong>FAQ {i}</strong><br/><br/>
<strong>Q: {faq.get('question', 'Question not available')}</strong><br/><br/>
<strong>A:</strong> {faq.get('answer', 'Answer not available')}
</div>
            """, unsafe_allow_html=True)
    else:
        st.info("No FAQs generated. Add 5-8 questions based on common user searches.")
    
    # ==== 5. ARTICLE SPECIFICATIONS SUMMARY ====
    st.markdown('<div class="section-header">5. ARTICLE SPECIFICATIONS SUMMARY</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
**Target Word Count:** {outline.get('total_word_count', '1,600-1,800')} words  
**Content Type:** {outline.get('content_type', 'Informational, evidence-based article')}  
**Target Audience:** {outline.get('target_audience', 'General audience seeking comprehensive information')}  
**Reading Level:** 8th-9th grade (accessible but informed)

**Content Goals:**
- Establish authority on the topic
- Drive organic traffic through targeted keywords
- Provide actionable, research-backed information
- Encourage engagement and social sharing

**Visual Requirements:**
- 1 featured image
- 3-5 custom infographics or charts
- Images optimized with alt text containing target keywords

**Citation Requirements:**
- Minimum 10-15 credible sources
- Link to peer-reviewed studies where possible
- Cite major authoritative organizations
- Include publication dates for credibility

**Update Frequency:** Review and update every 6 months with latest research

**Success Metrics:**
- Rank top 10 for primary keyword within 90 days
- Average time on page: 3+ minutes
- Bounce rate: <65%
- Social shares: 30+ in first month
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Export options at bottom
    st.markdown("---")
    st.markdown("### 📥 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col2:
        # Create text summary
        text_output = f"# {primary_keyword} - Content Strategy\n\n"
        text_output += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        text_output += f"## Article Outline\n\n"
        text_output += f"Title: {article_title}\n"
        text_output += f"Word Count: {outline.get('total_word_count', 'N/A')}\n\n"
        
        for i, section in enumerate(sections, 1):
            text_output += f"\n### {i}. {section.get('section_title', 'Untitled')}\n"
            text_output += f"Word Count: {section.get('suggested_word_count', 'N/A')}\n"
            text_output += f"Description: {section.get('short_description', 'N/A')}\n"
        
        st.download_button(
            label="📝 Download Text",
            data=text_output,
            file_name=f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    with col3:
        if st.button("🔄 Generate New Strategy", use_container_width=True):
            st.session_state.current_state = None
            st.session_state.generated_outline = None
            st.rerun()

def main():
    # App title
    st.title("🚀 AI Content Strategy Generator")
    st.markdown("*Generate comprehensive, template-based content strategies*")
    st.markdown("---")
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    serper_key = os.getenv("SERPER_API_KEY")
    
    if not openai_key:
        st.error("⚠️ OPENAI_API_KEY not found! Please set it in your .env file or environment variables.")
        st.stop()
    
    if not serper_key:
        st.warning("⚠️ SERPER_API_KEY not found. Competitor analysis will be limited.")
    
    # Two-column layout: Input on left, Output on right
    col_input, col_output = st.columns([1, 2])
    
    with col_input:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        
        st.markdown("### 📋 Input Configuration")
        
        # Mode selection
        mode = st.radio(
            "Generation Mode",
            ["Topic-based (with research)", "Keywords-based (no research)"],
            help="Topic-based performs full keyword research and competitor analysis"
        )
        
        st.markdown("---")
        
        # Input fields based on mode
        if mode == "Topic-based (with research)":
            st.markdown("#### 🔍 Enter Topic")
            topic = st.text_input(
                "Topic",
                placeholder="e.g., Coffee positives and negatives",
                help="Enter the main topic for content strategy",
                key="topic_input"
            )
            keywords_data = None
            
        else:
            st.markdown("#### 🔑 Enter Keywords")
            
            primary_kw = st.text_input(
                "Primary Keyword",
                placeholder="e.g., coffee positives and negatives",
                help="Main target keyword"
            )
            
            secondary_kw = st.text_area(
                "Secondary Keywords (one per line)",
                placeholder="coffee benefits\\ncoffee side effects\\ncoffee health",
                height=100
            )
            
            lsi_kw = st.text_area(
                "LSI Keywords (one per line)",
                placeholder="caffeine effects\\ncoffee research\\ncoffee consumption",
                height=100
            )
            
            keywords_data = {
                'primary': primary_kw.strip(),
                'secondary': [kw.strip() for kw in secondary_kw.split('\n') if kw.strip()],
                'lsi': [kw.strip() for kw in lsi_kw.split('\n') if kw.strip()]
            }
            
            topic = primary_kw
        
        st.markdown("---")
        
        # Settings
        st.markdown("#### ⚙️ Content Settings")
        
        word_count = st.slider(
            "Target Word Count",
            min_value=1000,
            max_value=5000,
            value=1800,
            step=100
        )
        
        tone = st.selectbox(
            "Tone",
            ["Professional", "Academic", "Casual", "Conversational"]
        )
        
        audience = st.selectbox(
            "Target Audience",
            ["General audience", "Professionals", "Students", "Health-conscious adults", "Experts"]
        )
        
        user_preferences = {
            "tone": tone.lower(),
            "target_audience": audience.lower()
        }
        
        st.markdown("---")
        
        # Generate button
        generate_clicked = st.button(
            "🚀 Generate Strategy",
            type="primary",
            disabled=st.session_state.processing,
            use_container_width=True
        )
        
        # Feedback section if outline exists
        if st.session_state.current_state:
            st.markdown("---")
            st.markdown("#### 💬 Refine Strategy")
            
            feedback = st.text_area(
                "Feedback",
                placeholder="e.g., Add more about health benefits, make it more technical",
                height=100
            )
            
            if st.button("🔄 Apply Feedback", disabled=st.session_state.processing, use_container_width=True):
                if feedback.strip():
                    st.session_state.processing = True
                    
                    try:
                        with st.spinner("Processing feedback..."):
                            updated_state = process_outline_feedback(
                                st.session_state.current_state,
                                feedback.strip()
                            )
                            
                            st.session_state.current_state = updated_state
                            st.session_state.generated_outline = updated_state.get('outline')
                            
                            st.success("✅ Feedback applied!")
                            time.sleep(1)
                            st.rerun()
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                    
                    finally:
                        st.session_state.processing = False
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_output:
        if generate_clicked:
            if not topic or not topic.strip():
                st.error("Please enter a topic or primary keyword")
            else:
                st.session_state.processing = True
                
                try:
                    with st.status("Generating content strategy...", expanded=True) as status:
                        st.write("🔍 Step 1: Analyzing keywords...")
                        
                        # Generate based on mode
                        if mode == "Topic-based (with research)":
                            st.write("🌐 Step 2: Researching competitors...")
                            st.write("🎯 Step 3: Analyzing content gaps...")
                            st.write("📝 Step 4: Creating outline...")
                            
                            result = generate_outline_from_topic(
                                topic=topic.strip(),
                                word_count=word_count,
                                user_preferences=user_preferences
                            )
                        else:
                            st.write("📝 Step 2: Creating outline...")
                            
                            result = generate_outline(
                                keywords_data=keywords_data,
                                word_count=word_count,
                                user_preferences=user_preferences
                            )
                        
                        st.session_state.current_state = result
                        st.session_state.generated_outline = result.get('outline')
                        
                        # Add to history
                        st.session_state.generation_history.append({
                            'timestamp': datetime.now().isoformat(),
                            'mode': mode,
                            'input': topic,
                            'result': result
                        })
                        
                        st.write("✅ Strategy generated successfully!")
                        status.update(label="✅ Generation complete!", state="complete")
                        
                        time.sleep(1)
                        st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Generation failed: {str(e)}")
                    st.exception(e)
                
                finally:
                    st.session_state.processing = False
        
        # Display output if available
        if st.session_state.current_state:
            display_template_output(st.session_state.current_state)
        else:
            st.info("👈 Enter a topic and click 'Generate Strategy' to begin")
            
            # Show example
            st.markdown("### 📖 Example Output")
            st.markdown("""
This tool will generate a comprehensive content strategy including:

1. **Competitor Analysis** - Top competing articles with strengths/weaknesses
2. **SEO Elements** - Optimized titles, meta descriptions, and keywords
3. **Article Structure** - Detailed sections with word counts, key points, and transitions
4. **FAQ Section** - 5-8 frequently asked questions with answers
5. **Specifications** - Content goals, visual requirements, and success metrics

The output follows professional content strategy templates used by top content marketing teams.
            """)

if __name__ == "__main__":
    main()
