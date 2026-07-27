#!/usr/bin/env python3
"""
Generate a large dataset (>50 GB) using Springer Nature Open Access API only.
Searches for papers related to 'diffusion models' and downloads all OA PDFs.
"""

import os
import time
import json
import csv
import requests
from typing import List, Dict, Optional
from tqdm import tqdm
from config import (
    SPRINGER_API_KEY,
    SPRINGER_API_URL,
    DATA_DIR,
    PDF_DIR,
    METADATA_CSV,
    METADATA_JSON
)

# ============================================================
# Override settings (you can change these)
# ============================================================
SEARCH_QUERY = "diffusion models"   # search term
MAX_RESULTS = 50000                 # target number of papers (adjust for size)
RESULTS_PER_PAGE = 100              # max per page (API limit is 100)
DOWNLOAD_DELAY = 0.5                # seconds between PDF downloads

# ============================================================
# Setup directories
# ============================================================
os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def search_springer(query: str, start: int, count: int) -> Optional[Dict]:
    """Query Springer Open Access API for papers."""
    params = {
        "api_key": SPRINGER_API_KEY,
        "q": query,
        "p": start,      # start index (1‑based)
        "s": count,      # number of results
    }
    try:
        resp = requests.get(SPRINGER_API_URL, params=params, timeout=30)
        if resp.status_code != 200:
            print(f"⚠️ API error: {resp.status_code} - {resp.text[:200]}")
            return None
        return resp.json()
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None

def get_all_papers(query: str, max_results: int) -> List[Dict]:
    """Paginate through Springer API to collect all papers."""
    papers = []
    total_fetched = 0
    page = 0

    print(f"Searching Springer for '{query}' (target: {max_results} papers)")
    while total_fetched < max_results:
        start = page * RESULTS_PER_PAGE + 1
        data = search_springer(query, start, RESULTS_PER_PAGE)
        if not data:
            break

        records = data.get('records', [])
        if not records:
            break

        # Extract relevant fields
        for rec in records:
            # Only keep papers with a PDF URL (OA)
            pdf_url = rec.get('pdf_url')
            if not pdf_url:
                continue
            papers.append({
                'title': rec.get('title', ''),
                'doi': rec.get('doi', ''),
                'authors': ', '.join([a.get('creator', '') for a in rec.get('creators', [])]),
                'publication_date': rec.get('publicationDate', ''),
                'abstract': rec.get('abstract', ''),
                'pdf_url': pdf_url,
                'url': rec.get('url', [{}])[0].get('value', '') if rec.get('url') else '',
            })

        total_fetched += len(records)
        page += 1
        print(f"   Fetched {len(records)} records (total {total_fetched})")

        # Stop if we have enough
        if total_fetched >= max_results:
            break

        # Respect rate limits
        time.sleep(0.2)

    return papers[:max_results]

def download_pdf(pdf_url: str, target_path: str) -> bool:
    """Download PDF from Springer."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(pdf_url, headers=headers, stream=True, timeout=60)
        if resp.status_code == 200:
            with open(target_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            # Verify PDF header
            with open(target_path, 'rb') as f:
                header = f.read(4)
                if header == b'%PDF':
                    return True
                else:
                    os.remove(target_path)
                    return False
    except Exception:
        pass
    return False

def main():
    # Step 1: Search Springer
    papers = get_all_papers(SEARCH_QUERY, MAX_RESULTS)
    print(f"\n✅ Retrieved {len(papers)} papers with PDF links.")

    if not papers:
        print("⚠️ No papers found. Check your query or API key.")
        return

    # Step 2: Save metadata
    with open(METADATA_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

    with open(METADATA_JSON, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2)

    print(f"📁 Metadata saved to {METADATA_CSV} and {METADATA_JSON}")

    # Step 3: Download PDFs
    print(f"\n📥 Starting PDF downloads to {PDF_DIR} ...")
    downloaded = 0
    total_size = 0

    for i, paper in enumerate(tqdm(papers, desc="Downloading")):
        # Sanitise filename
        safe_title = "".join(c for c in paper['title'] if c.isalnum() or c in " -_")[:80]
        pdf_path = os.path.join(PDF_DIR, f"{i:04d}_{safe_title}.pdf")
        if os.path.exists(pdf_path):
            downloaded += 1
            total_size += os.path.getsize(pdf_path)
            continue

        success = download_pdf(paper['pdf_url'], pdf_path)
        if success:
            downloaded += 1
            total_size += os.path.getsize(pdf_path)
        else:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)

        time.sleep(DOWNLOAD_DELAY)

    # Final report
    size_gb = total_size / (1024**3)
    print(f"\n🎉 Dataset generation complete!")
    print(f"   Total papers with PDFs: {downloaded}")
    print(f"   Total size: {size_gb:.2f} GB")
    if size_gb < 50:
        print(f"   ⚠️ Size is less than 50 GB. Increase MAX_RESULTS or adjust query.")

if __name__ == "__main__":
    main()