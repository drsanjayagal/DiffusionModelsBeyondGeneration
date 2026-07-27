# Diffusion Models Beyond Image Generation: A Comprehensive Survey of Visual Data Analysis

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21591678.svg)](https://doi.org/10.5281/zenodo.21591678)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Overview

This repository contains the complete **LaTeX source code, bibliography, figures, curated datasets, Python scripts, and supplementary materials** accompanying the survey paper:

> **Diffusion Models Beyond Image Generation: A Comprehensive Survey of Visual Data Analysis**

**Author:** Dr. Sanjay Agal

**Target Journal:** *Artificial Intelligence Review* (Springer)

---

## Abstract

Diffusion models have rapidly evolved from being powerful generative models to versatile frameworks capable of solving a wide range of **visual data analysis** tasks. This survey systematically reviews peer-reviewed journal publications between **2018 and 2026** from **IEEE, Springer Nature, Elsevier, and Wiley**, highlighting how diffusion models extend far beyond image synthesis.

The survey covers applications including:

- Medical Image Analysis
- Image Restoration
- Image Segmentation
- Remote Sensing
- Video Understanding
- Anomaly Detection
- Low-Level Vision
- Visual Recognition
- Image Enhancement
- Multimodal Vision
- Emerging Analytical Applications

In addition to summarizing recent advances, the paper presents a unified taxonomy, compares computational efficiency, analyzes benchmark datasets, identifies research challenges, and discusses future directions for diffusion-based visual intelligence.

---

# Repository Structure

```text
DiffusionModelsBeyondGeneration/
│
├── LaTeX/
│   ├── main.tex
│   ├── sn-jnl.cls
│   └── sections/
│       ├── 01_introduction.tex
│       ├── 02_fundamentals.tex
│       ├── 03_taxonomy.tex
│       ├── 04_image_restoration.tex
│       ├── 05_medical_imaging.tex
│       ├── 06_remote_sensing.tex
│       ├── 07_video_analysis.tex
│       ├── 08_anomaly_detection.tex
│       ├── 09_low_level_vision.tex
│       ├── 10_future_directions.tex
│       ├── 11_discussion.tex
│       ├── 12_limitations.tex
│       └── 13_conclusion.tex
│
├── bib/
│   └── references.bib
│
├── figures/
│   ├── taxonomy.pdf
│   ├── performance_comparison.pdf
│   ├── computational_cost.pdf
│   ├── application_domains.pdf
│   └── ...
│
├── datasets/
│   ├── metadata.csv
│   └── metadata.json
│
├── code/
│   ├── generate_dataset.py
│   └── utils/
│       ├── paper_fetcher.py
│       ├── taxonomy_builder.py
│       └── metadata_processor.py
│
├── data/
│
├── README.md
├── LICENSE
└── .gitignore
```

---

# Features

- Comprehensive survey of diffusion models for visual data analysis
- Coverage of peer-reviewed journal literature (2018–2026)
- Unified taxonomy of diffusion model applications
- Benchmark comparison across multiple vision tasks
- Computational cost analysis
- Curated metadata of surveyed publications
- Complete LaTeX source for manuscript reproduction
- Python utilities for dataset generation and metadata processing

---

# Dataset

The repository includes a carefully curated dataset of **40+ high-impact peer-reviewed journal publications** that form the foundation of this survey.

## Coverage

- **Publication Years:** 2018–2026
- **Publishers:**
  - IEEE
  - Springer Nature
  - Elsevier
  - Wiley

## Available Formats

- `metadata.csv`
- `metadata.json`

## Metadata Fields

- Paper Title
- Authors
- Journal
- Publication Year
- DOI
- Application Domain
- Task Category
- Diffusion Model
- Dataset Used
- Key Contribution
- Performance Metrics

---

# Zenodo Archive

The complete dataset and supplementary material are permanently archived on Zenodo.

**DOI:** https://doi.org/10.5281/zenodo.21591678

Please cite the Zenodo archive when using the dataset.

---

# Code

The repository contains Python scripts for:

- Synthetic dataset generation
- Metadata preprocessing
- Paper metadata collection
- Taxonomy construction
- CSV/JSON conversion
- Benchmark preparation

---

## Requirements

- Python 3.8+
- pandas
- numpy
- requests
- tqdm
- faker
- arxiv
- semantic-scholar

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Usage

Generate a synthetic dataset:

```bash
python code/generate_dataset.py --n_papers 50000 --pdf_size_mb 1.2
```

Process metadata:

```bash
python code/utils/metadata_processor.py
```

Build taxonomy:

```bash
python code/utils/taxonomy_builder.py
```

---

# Citation

If you use this repository, dataset, or survey, please cite:

```bibtex
@article{Agal2026Diffusion,
  author  = {Agal, Sanjay},
  title   = {Diffusion Models Beyond Image Generation: A Comprehensive Survey of Visual Data Analysis},
  journal = {Artificial Intelligence Review},
  year    = {2026},
  note    = {In preparation},
  doi     = {10.5281/zenodo.21591678}
}
```

Dataset citation:

```bibtex
@misc{Agal2026Dataset,
  author = {Agal, Sanjay},
  title  = {Curated Dataset for "Diffusion Models Beyond Image Generation: A Comprehensive Survey of Visual Data Analysis"},
  year   = {2026},
  note   = {Zenodo},
  doi    = {10.5281/zenodo.21591678}
}
```

---

# License

This repository is released under the **MIT License**.

See the `LICENSE` file for complete licensing information.

---

# Acknowledgements

The author gratefully acknowledges the contributions of the global research community whose work has advanced diffusion models for computer vision and visual data analysis. This survey synthesizes findings from leading journals published by IEEE, Springer Nature, Elsevier, and Wiley to provide a comprehensive overview of this rapidly evolving field.

---

## Contact

**Dr. Sanjay Agal**

Professor & Head, Department of Artificial Intelligence & Data Science  
Parul University, Vadodara, Gujarat, India

Email: sanjay.agal32685@paruluniversity.ac.in

---

### Repository DOI

**https://doi.org/10.5281/zenodo.21591678**