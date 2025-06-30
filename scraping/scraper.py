import os
import json
import requests
import hashlib
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI

# Load .env once
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
)

DATA_DIR = "data/recipes"
os.makedirs(DATA_DIR, exist_ok=True)

def url_to_filename(url):
    return hashlib.sha256(url.encode()).hexdigest() + ".json"

def scrape_website(url):
    """
    Caches recipes in JSON files. If already scraped, loads from disk.
    Otherwise scrapes and saves result.
    """

    # --- Check if we already have it ---
    cache_file = os.path.join(DATA_DIR, url_to_filename(url))
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                print(f"✅ Loaded cached recipe for {url}")
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load cache: {e}")

    # --- ELSE: scrape as before ---
    print(f"🔎 Scraping new recipe for {url}")

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

    # 2. Parse HTML & grab title
    soup = BeautifulSoup(resp.text, "html.parser")
    page_title = soup.title.string.strip() if soup.title else "Untitled Recipe"

    # 3. Clean tags
    for tag in soup((
        "nav","footer","header","aside","script","style",
        "noscript","form","iframe","meta","link","button",
        "input","svg"
    )):
        tag.decompose()

    # 4. Extract visible text
    raw_text = soup.get_text(separator="\n", strip=True)
    lines = [l for l in raw_text.splitlines() if l.strip()]
    lines = [l for l in lines if len(l.split()) > 3]
    seen = set(); clean_lines = []
    for l in lines:
        if l not in seen:
            clean_lines.append(l); seen.add(l)
    raw_text = "\n".join(clean_lines)
    if len(raw_text) > 12000:
        raw_text = raw_text[:6000] + "\n...\n" + raw_text[-6000:]

    # 5. Build prompt
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

    # 6. Call LLM
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528:free",
            messages=[
                {"role": "system", "content": "You are a helpful JSON extractor."},
                {"role": "user",   "content": prompt}
            ],
            extra_headers={
                "HTTP-Referer":"https://yourprojectsite.com",
                "X-Title":"ChefFlow"
            },
        )
        answer = completion.choices[0].message.content.strip()
    except Exception as e:
        print("❌ DeepSeek error:", e)
        return {"title":"Error", "steps":["Failed to extract recipe."]}

    # 7. Parse LLM JSON
    try:
        parsed = json.loads(answer)
        title = parsed.get("title") or page_title
        steps = parsed.get("steps", [])
        if not isinstance(steps, list) or not steps:
            steps = ["Sorry, no steps found."]
    except Exception as e:
        print("❌ JSON parse error:", e)
        print("Raw answer was:", answer)
        return {"title":page_title,
                "steps":[
                  "Extraction failed – here’s raw output:",
                  answer or "No response from LLM."
                ]}

    # 8. Save to disk
    to_save = {"title": title, "steps": steps}
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=2)
        print(f"💾 Saved recipe to {cache_file}")
    except Exception as e:
        print(f"⚠️ Failed to save cache: {e}")

    return to_save