import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Union
from urllib.parse import urlparse, parse_qs

def extract_target_url(url: str) -> str:
    """
    Extract the actual target URL from the malformed URL returned by DuckDuckGo.
    """
    parsed_url = urlparse(url)
    if "uddg" in parse_qs(parsed_url.query):
        return parse_qs(parsed_url.query)["uddg"][0]
    return url

def scrape_website(url: str) -> str:
    # Extract the actual target URL
    target_url = extract_target_url(url)

    # Prepend "https://" if the URL is missing a scheme
    if not target_url.startswith("http"):
        target_url = "https://" + target_url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(target_url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        return "\n".join([p.get_text(strip=True) for p in paragraphs])
    except Exception as e:
        print(f"[ERROR] Failed to scrape {target_url}: {e}")
        return ""

def duckduckgo_scrape(topic: str, count: int = 5, raw_text_only: bool = False) -> Union[str, List[Dict]]:
    query = topic.replace(" ", "+")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] DuckDuckGo request failed: {e}")
        return [] if not raw_text_only else ""

    soup = BeautifulSoup(res.text, "html.parser")
    results = soup.find_all("div", class_="result__body", limit=count)

    structured_results = []

    for result in results:
        title_tag = result.find("a", class_="result__a")
        snippet_tag = result.find("a", class_="result__snippet")
        link = title_tag.get("href") if title_tag else None
        title = title_tag.get_text(strip=True) if title_tag else "No Title"
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else "No snippet"

        # Scrape the actual website
        if link:
            content = scrape_website(link)
            structured_results.append({
                "title": title,
                "link": link,
                "snippet": snippet,
                "content": content
            })

    if raw_text_only:
        return "\n".join([f"{item['title']}: {item['snippet']}" for item in structured_results])
    else:
        return structured_results

