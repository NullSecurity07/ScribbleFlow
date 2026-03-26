def summarize_prompt(research_text: str, tone: str, audience: str) -> str:
    return f"""
You are a research analyst and content strategist.

 Objective:
Analyze the provided research thoroughly and extract deep, insight-rich information suitable for a company blog post.

 Your tasks:
- Identify and summarize **core trends**, **noteworthy patterns**, and **relevant data points**.
- Present **objective, neutral insights** that are useful for crafting content aimed at a professional audience.
- Highlight potential **blog-relevant content angles** based on the research, suitable for informing or educating readers.
- Avoid adding personal opinions, speculative takes, or persuasive commentary.

 Output Structure:
1. Executive Summary — 2–3 lines capturing the main theme of the research.
2. Key Trends & Insights — Bullet points (4–6), each with 1–2 lines explaining the trend.
3. Supporting Facts & Data — Bullet points with clear stats, observations, or study findings.
4. Potential Content Angles — Bullet points suggesting neutral, informative blog directions based on the data.

 Tone: {tone}  
 Target Audience: {audience}  
 Research Source:  
{research_text}

"""

def outline_prompt(summary: str, topic: str, tone: str, audience: str, max_words: int) -> str:
    return f"""
Act as a senior SEO content strategist and professional blogger.

Your task is to create a comprehensive, SEO-optimized blog outline on the topic: "{topic}".

Total target word count: {max_words} words

Requirements:
- Distribute word count appropriately across sections
- Use clear H2 and H3 headers following a logical structure
- Naturally incorporate keyword-rich section titles
- Include estimated word count per section
- Optimize structure for SEO performance

Constraints:
- Total content must not exceed {max_words} words
- Maintain {tone} tone for {audience} audience
- No need to include meta data

Context for narrative alignment:
{summary}
"""

def section_prompt(header: str, tone: str, audience: str, max_words: int, section_count: int) -> str:
    target_words = max_words // section_count
    return f"""
Write a blog section titled "{header}" with structured clarity and depth.

Tone: {tone}
Audience: {audience}
Target length: ~{target_words} words

Content Structure:
1. Introductory paragraph
2. 3-5 key sub-sections (## headers)
3. Examples and actionable takeaways
4. Concise conclusion

Guidelines:
- Keep content focused and scannable
- Use bullet points for lists
- Bold key terms
- Maintain professional voice
- Stay within {target_words}±100 words
"""

def seo_enhance_prompt(draft: str, topic: str, tone: str, audience: str) -> str:
    return f"""
Task: Refine the following blog draft to meet high editorial standards suitable for publication on a company website. Apply the following directives meticulously:
 Structural Enhancements

    Hook: Add a powerful opening hook — emotionally resonant or insight-driven — to immediately capture attention.

    SEO Title: Improve the title with SEO in mind. Ensure it’s clear, keyword-rich (if applicable), and click-worthy.

    Meta Description: Write a concise meta description (max 160 characters) summarizing the article with clarity and click potential.

    Formatting: Structure cleanly in Markdown — use headers (#, ##, etc.), bullet points, numbered lists, and blockquotes where needed.

    Readability: Ensure high readability — short paragraphs, varied sentence length, active voice, and accessible vocabulary (aim for grade 8–10 readability).

 Tone & Audience Alignment

    Match the tone as specified in {tone} — professional, conversational, technical, persuasive, etc.

    Adapt language, metaphors, and examples to connect with the target audience: {audience}.

 Considerations

    No CTA is required unless it emerges naturally from the content.

    Optimize for a company blog — think trust, authority, clarity.

    Avoid unnecessary buzzwords, emojis, or slang unless explicitly aligned with tone/audience.

 Input Parameters

    Topic: {topic}

    Tone: {tone}

    Audience: {audience}

    Draft: {draft}
"""

