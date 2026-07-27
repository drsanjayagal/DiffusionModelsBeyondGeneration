#!/usr/bin/env python3
"""
Generate a large dataset from arXiv using the official arxiv library.
"""

import os
import time
import json
import csv
import requests
from typing import List, Dict, Set
from tqdm import tqdm
import arxiv

from config import (
    DATA_DIR,
    PDF_DIR,
    METADATA_CSV,
    METADATA_JSON,
    MAX_PAPERS,
    DOWNLOAD_DELAY,
    SEARCH_TERMS
)

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

def fetch_arxiv_papers(terms: List[str], max_results: int) -> List[Dict]:
    papers = []
    seen_ids: Set[str] = set()
    total_fetched = 0

    client = arxiv.Client()

    for term in terms:
        if total_fetched >= max_results:
            break

        print(f"\n🔍 arXiv searching: '{term}'")
        per_term_limit = min(1000, max_results - total_fetched)   # avoid huge batches
        search = arxiv.Search(
            query=term,
            max_results=per_term_limit,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        term_fetched = 0
        for result in client.results(search):
            paper_id = result.entry_id.split('/')[-1]
            if paper_id in seen_ids:
                continue
            seen_ids.add(paper_id)
            print(f"   📄 Fetched: {result.title[:60]}...")   # show progress

            pdf_url = result.pdf_url
            authors = [a.name for a in result.authors]

            papers.append({
                'title': result.title,
                'arxiv_id': paper_id,
                'doi': result.doi if result.doi else '',
                'authors': ', '.join(authors),
                'publication_date': result.published.strftime('%Y-%m-%d') if result.published else '',
                'abstract': result.summary,
                'pdf_url': pdf_url,
                'source': 'arXiv',
                'url': result.entry_id,
            })

            term_fetched += 1
            total_fetched += 1
            if total_fetched >= max_results:
                break

        print(f"   ✅ From '{term}': {term_fetched} papers")

    return papers[:max_results]

def download_pdf(pdf_url: str, target_path: str) -> bool:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(pdf_url, headers=headers, stream=True, timeout=60)
        if resp.status_code == 200:
            with open(target_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            with open(target_path, 'rb') as f:
                if f.read(4) == b'%PDF':
                    return True
                else:
                    os.remove(target_path)
                    return False
    except Exception as e:
        print(f"   ❌ Download failed: {e}")
    return False

def main():
    print("=" * 60)
    print("📚 arXiv Dataset Generator (Real Academic Papers)")
    print("=" * 60)

    papers = fetch_arxiv_papers(SEARCH_TERMS, MAX_PAPERS)
    print(f"\n✅ Retrieved {len(papers)} unique papers from arXiv.")

    if not papers:
        print("❌ No papers retrieved. Please check your search terms or internet.")
        return

    with open(METADATA_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
    with open(METADATA_JSON, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=2)
    print(f"📁 Metadata saved to {METADATA_CSV} and {METADATA_JSON}")

    print(f"\n📥 Starting PDF downloads to {PDF_DIR} ...")
    downloaded = 0
    total_size = 0

    for i, paper in enumerate(tqdm(papers, desc="Downloading PDFs")):
        safe_title = "".join(c for c in paper['title'][:80] if c.isalnum() or c in " -_")
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

    size_gb = total_size / (1024 ** 3)
    print("\n" + "=" * 60)
    print("🎉 Dataset generation complete!")
    print(f"   📄 Total papers: {len(papers)}")
    print(f"   📥 PDFs downloaded: {downloaded}")
    print(f"   💾 Total size: {size_gb:.2f} GB")

    if size_gb < 50:
        print("\n⚠️ Size below 50 GB. Increase MAX_PAPERS or add more search terms.")

if __name__ == "__main__":
    main()