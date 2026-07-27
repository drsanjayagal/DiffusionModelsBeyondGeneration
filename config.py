# config.py
# Configuration for arXiv dataset generator

# ------------------------------------------------------------------
# Output directories
# ------------------------------------------------------------------
DATA_DIR = "data"
PDF_DIR = f"{DATA_DIR}/pdfs"
METADATA_CSV = f"{DATA_DIR}/metadata.csv"
METADATA_JSON = f"{DATA_DIR}/metadata.json"

# ------------------------------------------------------------------
# Dataset size parameters (adjust to reach >50 GB)
# ------------------------------------------------------------------
MAX_PAPERS = 50000          # target number of papers
DOWNLOAD_DELAY = 0.5        # seconds between PDF downloads (rate limiting)

# ------------------------------------------------------------------
# Search keywords (expand to get more papers)
# ------------------------------------------------------------------
SEARCH_TERMS = [
    "diffusion models",
    "generative models",
    "denoising",
    "score-based",
    "neural networks",
    "deep learning",
    "generative adversarial networks",
    "variational autoencoder",
    "probabilistic models"
]