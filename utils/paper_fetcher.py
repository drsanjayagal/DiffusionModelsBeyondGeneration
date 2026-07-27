import time
import os
import requests
import arxiv
from semanticscholar import SemanticScholar
from typing import Optional, Dict
import re
from config import *
from urllib.parse import quote

sch = SemanticScholar()

# ----------------------------
# Helper: fetch PDF from a URL
# ----------------------------
def fetch_pdf_from_url(pdf_url: str, target_path: str) -> bool:
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(pdf_url, headers=headers, stream=True, timeout=60)
        if resp.status_code == 200:
            # Check if it's a PDF (by magic bytes)
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
        return False

# ----------------------------
# Springer Nature Open Access
# ----------------------------
def fetch_pdf_from_springer(doi: str, target_path: str) -> bool:
    """Fetch PDF via Springer Nature OA API using DOI."""
    if not SPRINGER_API_KEY:
        return False
    try:
        # Search by DOI
        url = f"{SPRINGER_API_URL}?api_key={SPRINGER_API_KEY}&q=doi:{doi}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return False
        data = resp.json()
        records = data.get('records', [])
        if not records:
            return False
        # The PDF URL is in the 'pdf_url' field (if OA)
        pdf_url = records[0].get('pdf_url')
        if pdf_url:
            return fetch_pdf_from_url(pdf_url, target_path)
        # If not, try to get the fulltext URL
        fulltext = records[0].get('fulltext', {})
        pdf_url = fulltext.get('url')
        if pdf_url:
            return fetch_pdf_from_url(pdf_url, target_path)
    except Exception:
        pass
    return False

# ----------------------------
# IEEE Xplore Open Access
# ----------------------------
def fetch_pdf_from_ieee(doi: str, target_path: str) -> bool:
    """Fetch PDF via IEEE Xplore OA API using DOI."""
    if not IEEE_API_KEY:
        return False
    try:
        # IEEE API expects DOI without 'doi.org/'
        doi_clean = doi.replace('doi.org/', '').replace('https://', '').replace('http://', '')
        # Construct query
        url = (f"{IEEE_API_URL}?apikey={IEEE_API_KEY}"
               f"&format=json&doi={doi_clean}&article=true")
        resp = requests.get(url)
        if resp.status_code != 200:
            return False
        data = resp.json()
        articles = data.get('articles', [])
        if not articles:
            return False
        # For OA articles, the PDF link is often in 'pdf_link' field
        pdf_url = articles[0].get('pdf_link')
        if pdf_url:
            return fetch_pdf_from_url(pdf_url, target_path)
    except Exception:
        pass
    return False

# ----------------------------
# Unpaywall (generic OA resolver)
# ----------------------------
def fetch_pdf_from_unpaywall(doi: str, target_path: str) -> bool:
    """Use Unpaywall to find OA PDF URL."""
    if not UNPAYWALL_EMAIL:
        return False
    try:
        url = f"https://api.unpaywall.org/v2/{doi}?email={UNPAYWALL_EMAIL}"
        resp = requests.get(url)
        if resp.status_code != 200:
            return False
        data = resp.json()
        oa_location = data.get('best_oa_location')
        if not oa_location:
            return False
        pdf_url = oa_location.get('url_for_pdf')
        if pdf_url:
            return fetch_pdf_from_url(pdf_url, target_path)
    except Exception:
        pass
    return False

# ----------------------------
# Get DOI from Semantic Scholar
# ----------------------------
def get_doi_from_semantic(title: str) -> Optional[str]:
    """Search Semantic Scholar by title and return DOI if available."""
    time.sleep(SEMANTIC_SCHOLAR_DELAY)
    try:
        results = sch.search_paper(title, limit=1)
        if not results:
            return None
        paper = results[0]
        if hasattr(paper, 'doi') and paper.doi:
            return paper.doi
        # Also try the externalIds
        if hasattr(paper, 'externalIds'):
            ext = paper.externalIds
            if 'DOI' in ext:
                return ext['DOI']
    except Exception:
        pass
    return None

# ----------------------------
# Main get_paper_data (enhanced)
# ----------------------------
def get_paper_data(title: str) -> Dict:
    """Fetch metadata and PDF URL from multiple sources."""
    # Try Semantic Scholar first
    meta = get_metadata_semantic(title)
    if not meta:
        # Fallback to arXiv
        arxiv_id = get_arxiv_id_from_title(title)
        if arxiv_id:
            meta = {
                "title": title,
                "arxiv_id": arxiv_id,
                "doi": None,
                "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "authors": "",
                "year": None,
                "citation_count": None,
                "abstract": None,
                "url": f"https://arxiv.org/abs/{arxiv_id}"
            }
        else:
            # Still keep a record without PDF source
            meta = {"title": title, "arxiv_id": None, "doi": None, "pdf_url": None,
                    "authors": "", "year": None, "citation_count": None,
                    "abstract": None, "url": None}

    # If we have a DOI, add it to meta (if not already present)
    if meta.get('doi') is None and meta.get('paper_id'):
        # Try to get DOI from Semantic Scholar paper ID (or directly from title)
        doi = get_doi_from_semantic(title)
        if doi:
            meta['doi'] = doi

    # Ensure pdf_url is set to None if not found
    if meta.get('pdf_url') is None:
        meta['pdf_url'] = None

    return meta

# ----------------------------
# Master PDF download function (new)
# ----------------------------
def download_pdf(paper: Dict, target_dir: str) -> Optional[str]:
    """
    Download PDF from any available source.
    Returns file path if successful, else None.
    """
    title = paper.get('title')
    arxiv_id = paper.get('arxiv_id')
    doi = paper.get('doi')
    pdf_url = paper.get('pdf_url')

    # Sanitise filename
    safe_title = "".join(c for c in title if c.isalnum() or c in " -_")[:100]
    arxiv_part = arxiv_id if arxiv_id else "noarxiv"
    pdf_path = os.path.join(target_dir, f"{arxiv_part}_{safe_title}.pdf")
    if os.path.exists(pdf_path):
        return pdf_path

    # Priority 1: Direct PDF URL from Semantic Scholar
    if pdf_url and pdf_url.startswith('http'):
        if fetch_pdf_from_url(pdf_url, pdf_path):
            return pdf_path

    # Priority 2: arXiv
    if arxiv_id:
        pdf_url_arxiv = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        if fetch_pdf_from_url(pdf_url_arxiv, pdf_path):
            return pdf_path

    # Priority 3: Springer OA (if DOI available)
    if doi:
        if fetch_pdf_from_springer(doi, pdf_path):
            return pdf_path

    # Priority 4: IEEE OA (if DOI available)
    if doi:
        if fetch_pdf_from_ieee(doi, pdf_path):
            return pdf_path

    # Priority 5: Unpaywall (generic OA resolver)
    if doi:
        if fetch_pdf_from_unpaywall(doi, pdf_path):
            return pdf_path

    # All failed
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    return None