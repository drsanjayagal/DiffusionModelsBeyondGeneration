import re
from typing import List, Dict

def parse_papers_from_readme(readme_path: str) -> List[Dict]:
    """Extract title, URL, category, subcategory from survey README."""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'\*\*', '', content)
    content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', content)

    papers = []
    current_category = "Uncategorized"
    current_subcategory = "Uncategorized"

    lines = content.split('\n')
    cat_pattern = re.compile(r'^##\s+(.*)')
    subcat_pattern = re.compile(r'^###\s+(.*)')
    subsub_pattern = re.compile(r'^####\s+(.*)')
    paper_pattern = re.compile(r'^[-*]\s+(.*?)(?:\s*\(.*?\))?$')

    for line in lines:
        line = line.strip()
        if not line:
            continue
        m = cat_pattern.match(line)
        if m:
            current_category = m.group(1).strip()
            current_subcategory = "Uncategorized"
            continue
        m = subcat_pattern.match(line)
        if m:
            current_subcategory = m.group(1).strip()
            continue
        m = subsub_pattern.match(line)
        if m:
            current_subcategory = m.group(1).strip()
            continue
        m = paper_pattern.match(line)
        if m:
            title = m.group(1).strip()
            url_match = re.search(r'\((https?://[^)]+)\)', line)
            url = url_match.group(1) if url_match else ""
            papers.append({
                "title": title,
                "url": url,
                "category": current_category,
                "subcategory": current_subcategory
            })
    return papers