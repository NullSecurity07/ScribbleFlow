import os
from research import duckduckgo_scrape
from writer import summarize, generate_outline, expand_outline, refine_blog, clean_blog, enhance_seo

def save_blog(content: str, topic: str):
    safe_name = topic.lower().replace(" ", "_")
    os.makedirs("output", exist_ok=True)
    with open(f"output/{safe_name}.md", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Blog saved to output/{safe_name}.md")


def main():
    try:
        topic = input("📝 Enter your blog topic: ").strip()
        tone = input("🎭 Enter the tone of the blog (e.g., formal, casual, professional): ").strip()
        audience = input("👥 Enter the target audience (e.g., beginners, experts, general readers): ").strip()
        style = input("🖋️ Enter the writing style (e.g., narrative, technical, conversational): ").strip()
        max_words = int(input("🔢 Enter maximum word count (e.g., 1500): ").strip())

        if not topic:
            raise ValueError("Topic cannot be empty.")

        print(f"\n🔍 Researching: {topic}")
        research = duckduckgo_scrape(topic)

        print("🧠 Summarizing...")
        summary = summarize(research, tone, audience, style)

        print("📋 Generating Outline...")
        outline = generate_outline(summary, topic, tone, audience, style, max_words)
        print(outline)

        print("✍️ Writing Sections...")
        draft = expand_outline(outline, tone, audience, style, max_words)

        print("📈 SEO Enhancing...")
        final_blog = enhance_seo(draft, topic, tone, audience, style)

        save_blog(final_blog, topic)

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
