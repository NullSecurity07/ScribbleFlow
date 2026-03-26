from typing import Dict
import time
from ollama_client import call_ollama, OLLAMA_MODEL
from prompts import summarize_prompt, outline_prompt, section_prompt, seo_enhance_prompt


def summarize(research: str, tone: str, audience: str, style: str) -> str:
    prompt = summarize_prompt(research, tone, audience)
    return call_ollama(prompt, model=OLLAMA_MODEL)


def generate_outline(summary: str, topic: str, tone: str, audience: str, style: str, max_words: int) -> str:
    prompt = outline_prompt(summary, topic, tone, audience, max_words)
    return call_ollama(prompt, model=OLLAMA_MODEL)

def expand_outline(outline: str, tone: str, audience: str, style: str, max_words: int) -> str:
    final = ""
    estimated_total = 0
    for line in outline.strip().splitlines():
        if line.strip().startswith("H"):
            header = line.lstrip("H123456. ").strip()
            content = call_ollama(
                section_prompt(header, tone, audience, max_words, len(outline.strip().splitlines())),
                model=OLLAMA_MODEL
            )
            final += f"## {header}\n\n{content}\n\n"
            time.sleep(1)
    return final.strip()


def enhance_seo(draft: str, topic: str, tone: str, audience: str, style: str) -> str:
    prompt = seo_enhance_prompt(draft, topic, tone, audience)
    return call_ollama(prompt, model=OLLAMA_MODEL)


def review_blog(blog: str, topic: str) -> str:
    prompt = f"""
You are a high-level content evaluator agent, combining the roles of a professional blogger, SEO analyst, and engagement strategist. Assume the following context:

- The blog is written for a company's website.
- Audience tone, SEO target keywords, and writing goals have already been defined by upstream modules.
- Your role is to **analyze the blog post** and return structured, actionable feedback for optimization before publishing.

Perform the following tasks on the blog titled: "{topic}"

---

1.  **Scoring (1-10 scale)**:
   - **Readability** – Clarity, structure, pacing, and paragraph flow
   - **SEO** – Keyword placement, heading structure, meta content, internal linking potential
   - **Engagement** – Emotional hook, storytelling, calls to action, retention mechanics

2.  **Improvement Suggestions**:
   - Rewrite weak areas or give line-level examples if needed
   - Recommend structural or SEO improvements (e.g., better headers, more visuals, stronger intro/CTA)

3.  **Strategic Commentary**:
   - Does the content deliver on its apparent goal (e.g., inform, convert, position authority)?
   - Would a reader feel compelled to trust and engage with the brand?
   - Any standout strengths worth preserving?

Return your output in structured Markdown with clearly separated sections.

---

Now evaluate the blog below:
{blog}
"""
    return call_ollama(prompt, model=OLLAMA_MODEL)


def refine_blog(blog: str, feedback: str, tone: str, audience: str, style: str) -> str:
    prompt = f"""
Refine the following company blog post based on user-defined tone and audience. This refinement must:
 Objectives:

    Improve Readability:
    Use shorter sentences, clean transitions, and scan-friendly structure (bullet points, subheaders, etc.).

    Enhance SEO:
    Apply on-page SEO best practices — include relevant keywords, optimize H1/H2/H3 structure, improve meta description, and suggest a clean URL slug.

    Increase Engagement:
    Strengthen the hook in the introduction, maintain a conversational yet authoritative flow, and close with a subtle call to thought or action — without direct promotion.

 Constants:

    Tone: {tone}
    Audience: {audience}
    Platform: Company Website (No links required)
    Style: Uniform across all articles; maintain consistency in voice, pacing, and vocabulary.

 Blog Draft:
{blog}

 Feedback to Address:
{feedback}

 Final Output Format:

    Return in Markdown

    Include:

        Suggested title (H1)
        SEO-optimized meta description (≤ 160 characters)
        SEO-friendly URL slug
        Clear headings (H2/H3)
        Bullet points or numbered lists for readability
        Clean formatting for direct publishing

Do not include external or internal links.
"""
    return call_ollama(prompt, model=OLLAMA_MODEL)


def clean_blog(blog: str, topic: str) -> str:
    # Add H1 title
    blog = f"# {topic}\n\n{blog}"

    # Add meta description as HTML comment
    meta_description = f"<!-- Meta Description: A detailed blog on {topic} with insights, examples, and actionable tips. -->\n\n"
    blog = meta_description + blog

    # Remove unnecessary whitespace
    blog = "\n".join([line.strip() for line in blog.splitlines() if line.strip()])

    # Normalize markdown spacing
    blog = blog.replace("\n\n\n", "\n\n")

    return blog
