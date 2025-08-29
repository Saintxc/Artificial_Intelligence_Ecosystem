import os
import requests
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

HARDCODED_URL = "https://en.wikipedia.org/wiki/Grizzly_bear"
OUTPUT_FILE = "Selected_Document.txt"

def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Referer": "https://en.wikipedia.org/",
    })
    retry = Retry(
        total=4, connect=2, backoff_factor=1.0,
        status_forcelist=(403, 429, 500, 502, 503, 504),
        allowed_methods=("GET",), raise_on_status=False,
    )
    s.mount("https://", HTTPAdapter(max_retries=retry))
    s.mount("http://", HTTPAdapter(max_retries=retry))
    return s

def fetch_and_extract() -> str:
    try:
        resp = _session().get(HARDCODED_URL, timeout=20, allow_redirects=True)
    except requests.RequestException as e:
        print(f"Failed to fetch page due to a network error: {e}")
        return ""

    if resp.status_code != 200:
        print(f"Failed to fetch page. HTTP status code: {resp.status_code}")
        return ""

    soup = BeautifulSoup(resp.content, "html.parser")

    # ====== KEY CHANGE: select from the whole document ======
    # Grab all <p> that live anywhere inside a <div class="mw-parser-output">
    paragraphs = soup.select("div.mw-parser-output p")
    # ========================================================

    texts = []
    for p in paragraphs:
        t = p.get_text(" ", strip=True)
        if t:
            texts.append(t)

    extracted_text = "\n\n".join(texts)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
        f.write(extracted_text)

    print("Success: Page fetched (HTTP 200) and content written to Selected_Document.txt")
    print(f"Paragraphs found: {len(paragraphs)} | Characters written: {len(extracted_text)}")
    print(f"Output path: {os.path.abspath(OUTPUT_FILE)}")
    if extracted_text:
        print("Preview:", extracted_text[:300].replace("\n", " "))

    return extracted_text

def main():
    _ = fetch_and_extract()

if __name__ == "__main__":
    main()