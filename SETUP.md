# 🛠️ Setup Guide

Complete setup instructions for the FIFA 21 ETL Pipeline project.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Run](#first-run)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.8 or higher (3.13.9 recommended)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: 500MB free space

### Software Dependencies

- Python 3.8+
- pip (Python package manager)
- Git (for cloning the repository)

### Check Your Python Version

```bash
python --version
# Should show: Python 3.8.x or higher
```

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: `brew install python3`
- **Linux**: `sudo apt-get install python3 python3-pip`

---

## Installation

### Step 1: Clone the Repository

```bash
# Clone the project
git clone https://github.com/arthur7657/fifa21_etl_pipeline.git

# Navigate to project directory
cd fifa21_etl_pipeline
```

### Step 2: Create Virtual Environment

**Windows:**
```cmd
# Create virtual environment
python -m venv project1_env

# Activate virtual environment
project1_env\Scripts\activate

# Your prompt should now show (project1_env)
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv project1_env

# Activate virtual environment
source project1_env/bin/activate

# Your prompt should now show (project1_env)
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed pandas-2.x.x openpyxl-3.x.x pyarrow-12.x.x pytest-7.x.x pytest-cov-4.x.x
```

### Step 4: Verify Installation

```bash
# Check installed packages
pip list

# You should see:
# pandas, openpyxl, pyarrow, pytest, pytest-cov
```

---

## Configuration

### Project Structure Verification

Ensure your project has this structure:

```
fifa21_etl_pipeline/
├── eti_pipeline/
│   └── src/
│       ├── extract/
│       ├── transform/
│       ├── load/
│       └── utillis/
├── tests/
├── data/
│   ├── raw/
│   │   └── fifa21 raw data v2.csv  ← Important!
│   └── processed/  ← Will be created
├── logs/           ← Will be created
├── main.py
└── requirements.txt
```

### Data File Setup

1. **Verify raw data file exists:**
   ```bash
   # Windows
   dir "data\raw\fifa21 raw data v2.csv"
   
   # macOS/Linux
   ls "data/raw/fifa21 raw data v2.csv"
   ```

2. **If file is missing:**
   - Download from: [Kaggle FIFA 21 Dataset](https://www.kaggle.com/datasets/stefanoleone992/fifa-21-complete-player-dataset)
   - Place in `data/raw/` folder
   - Ensure filename is exactly: `fifa21 raw data v2.csv`

### Optional: Configure Output Settings

Edit `main.py` to customize:

```python
# Change input file location
INPUT_FILE = "data/raw/your_custom_file.csv"

# Change output directory
OUTPUT_DIR = "data/processed/"
```

---

## First Run

### Step 1: Run the Pipeline

```bash
# Make sure virtual environment is activated
# You should see (project1_env) in your prompt

# Run the pipeline
python main.py
```

### Step 2: Expected Output

You should see:

```
================================================================
FIFA 21 Data Pipeline
================================================================
Started at: YYYY-MM-DD HH:MM:SS
================================================================

STEP 1: EXTRACT
================================================================
📥 Extract: Loading data from: fifa21 raw data v2.csv
📁 Location: C:\...\data\raw\fifa21 raw data v2.csv
✅ Loaded 18,979 rows x 77 columns
✅ Extraction complete!

STEP 2: TRANSFORM
================================================================
🧹 Transform complete!
📊 Cleaned data: 18,979 rows x 73 columns

STEP 3: LOAD
================================================================
Saving cleaned data in 4 format(s)...
✅ CSV saved: C:\...\data\processed\fifa21_cleaned.csv
✅ Excel saved: C:\...\data\processed\fifa21_cleaned.xlsx
✅ JSON saved: C:\...\data\processed\fifa21_cleaned.json
✅ Parquet saved: C:\...\data\processed\fifa21_cleaned.parquet
```

### Step 3: Verify Output Files

```bash
# Check output directory
ls data/processed/

# You should see:
# fifa21_cleaned.csv
# fifa21_cleaned.xlsx
# fifa21_cleaned.json
# fifa21_cleaned.parquet
```

---

## Verification

### Run Tests

```bash
# Run all tests
pytest

# Expected output:
# ========================= 26 passed in 1.32s =========================
```

### Check Test Coverage

```bash
# Generate coverage report
pytest --cov=eti_pipeline --cov-report=term-missing --cov-report=html

# Expected coverage: ~28%
```

### View Coverage Report

```bash
# Open HTML coverage report
# Windows:
start htmlcov/index.html

# macOS:
open htmlcov/index.html

# Linux:
xdg-open htmlcov/index.html
```

### Verify Log Files

```bash
# Check logs directory
ls logs/

# You should see:
# pipeline_YYYYMMDD_HHMMSS.log
```

---

## Troubleshooting

### Common Issues

#### Issue: "Python not found"
```bash
# Try python3 instead of python
python3 --version
python3 -m venv project1_env
```

#### Issue: "pip: command not found"
```bash
# Use python -m pip instead
python -m pip install -r requirements.txt
```

#### Issue: "Module not found: pandas"
```bash
# Ensure virtual environment is activated
# Windows:
project1_env\Scripts\activate

# Then reinstall:
pip install -r requirements.txt
```

#### Issue: "File not found: fifa21 raw data v2.csv"
```bash
# Check file exists and name is correct
dir "data\raw"  # Windows
ls data/raw/    # macOS/Linux

# File must be named exactly: "fifa21 raw data v2.csv"
# Note the space in the filename!
```

#### Issue: "Permission denied" when running tests
```bash
# Windows: Run as Administrator
# macOS/Linux: Check file permissions
chmod +x main.py
```

---

## Next Steps

After successful setup:

1. ✅ Read the [README.md](README.md) for project overview
2. ✅ Check [ERRORS.md](ERRORS.md) for common error solutions
3. ✅ Explore the output files in `data/processed/`
4. ✅ View logs in `logs/` directory
5. ✅ Customize the pipeline for your needs

---

## Getting Help

If you encounter issues:

1. **Check ERRORS.md** for common solutions
2. **Review logs** in `logs/` directory
3. **Run tests** to verify installation: `pytest -v`
4. **Open an issue** on [GitHub](https://github.com/arthur7657/fifa21_etl_pipeline/issues)

---

## Deactivating Virtual Environment

When you're done working:

```bash
# Deactivate virtual environment
deactivate

# Your prompt should return to normal (no project1_env prefix)
```

---

## Updating the Project

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade
```

---

**Setup complete!** 🎉 You're ready to use the FIFA 21 ETL Pipeline.
