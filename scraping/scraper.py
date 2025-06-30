import os
import json
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load .env once
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

def scrape_website(url):
    """
    Fast + robust recipe extractor via DeepSeek/OpenRouter.
    """

    # 1. Download page
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()

    # 2. Parse HTML & grab the real page <title>
    soup = BeautifulSoup(resp.text, "html.parser")
    page_title = soup.title.string.strip() if soup.title else "Untitled Recipe"

    # 3. Remove junk tags
    for tag in soup((
        "nav","footer","header","aside","script","style",
        "noscript","form","iframe","meta","link","button",
        "input","svg"
    )):
        tag.decompose()

    # 4. Extract visible text
    raw_text = soup.get_text(separator="\n", strip=True)

    # 5. Clean text for speed:
    #  - remove blank lines
    #  - remove short lines (<4 words)
    #  - dedupe repeated lines
    lines = [l for l in raw_text.splitlines() if l.strip()]
    lines = [l for l in lines if len(l.split()) > 3]
    seen = set(); clean_lines = []
    for l in lines:
        if l not in seen:
            clean_lines.append(l); seen.add(l)
    raw_text = "\n".join(clean_lines)

    # 6. Smart truncate only if enormous
    if len(raw_text) > 12000:
        raw_text = raw_text[:6000] + "\n...\n" + raw_text[-6000:]

    # 7. Build a crystal‑clear prompt
    prompt = f"""
You are a recipe extractor.  Extract the recipe in STRICT JSON:

Page Title:
{page_title}

Page Text:
{raw_text}

OUTPUT FORMAT (no extra keys, no commentary, valid JSON):
{{
  "title": "string",
  "steps": ["string", ...]
}}
Always fill in "title" and "steps" arrays only.
"""

    # 8. Call DeepSeek / OpenRouter
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "You are a helpful JSON extractor."},
                {"role": "user",   "content": prompt}
            ],
            extra_headers={"HTTP-Referer":"https://yourprojectsite.com",
                           "X-Title":"ChefFlow"},
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        print("❌ DeepSeek error:", e)
        return {"title":"Error", "steps":["Failed to extract recipe."]}

    # DEBUG (uncomment while tuning):
    # print("LLM answer:", answer)

    # 9. Parse JSON with fallback to page_title
    try:
        parsed = json.loads(answer)
        title = parsed.get("title") or page_title
        steps = parsed.get("steps", [])
        if not isinstance(steps, list) or not steps:
            steps = ["Sorry, no steps found."]
    except Exception as e:
        print("❌ JSON parse error:", e)
        # show raw LLM answer for debugging
        print("Raw answer was:", answer)
        return {"title":page_title,
                "steps":[
                  "Extraction failed – here’s raw output:",
                  answer or "No response from LLM."
                ]}

    # 10. (Optional) Save to disk for caching
    # Uncomment if you want a persistent copy
    # os.makedirs("data/recipes", exist_ok=True)
    # safe_fn = "".join(c for c in title if c.isalnum() or c in " _-").rstrip()
    # with open(f"data/recipes/{safe_fn}.json","w",encoding="utf-8") as f:
    #     json.dump({"title":title,"steps":steps}, f, indent=2)

    return {"title": title, "steps": steps}

