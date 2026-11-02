# ⚡ Exploratory Data Tool (`eda_tools`)

<div style="display: flex; align-items: flex-start;">
  <img src="https://techstack-generator.vercel.app/python-icon.svg" alt="icon" width="65" height="65" />
  <img src="assets/numpy-icon.svg" alt="NumPy" width="65" height="65" />
</div>

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](#)

> **A lightweight, zero-bloat automated EDA & data-health profiling dashboard for Jupyter, VS Code Interactive (`# %%`), and Google Colab.**

---

## 🎯 Why This Tool Was Made

Exploratory Data Analysis (EDA) usually presents a frustrating trade-off:

| Approach | The Problem |
| :--- | :--- |
| **Vanilla Pandas** (`df.info()`, `df.describe()`) | ❌ Fragmented, monochrome, purely tabular, lacks automated sanity alerts, requires 20+ manual repetitive lines. |
| **Heavy Profilers** (`ydata-profiling`, `sweetviz`) | ❌ Bloated dependencies, takes minutes to generate multi-megabyte HTML reports, and frequently crashes browser tabs on medium/large datasets. |
| **⚡ `eda_tools`** | ✅ **Instant, lightweight, dark-themed dashboard embedded in your notebook in 1 line of code.** |

`eda_tools` was built to give data scientists, analysts, and ML engineers an **instant executive health summary** of any tabular dataset without slowing down their iterative workflow.

---

## ✨ Key Features

- 🖥️ **Executive Health Dashboard**: Instant KPI cards for total rows, columns, memory footprint (deep inspection), duplicate rows, and missing cell percentages.
- 📋 **Enhanced Schema & Heatmap**: A color-coded overview of column data types, null counts, null percentages, cardinality, and sample non-null values.
- 🚨 **Smart Feature Engineering Alerts**:
  - Detects **zero-variance / constant columns** (wasted memory & compute).
  - Flags **unparsed datetime strings** stored as generic `object` types.
  - Identifies **high-cardinality ID / UUID columns**.
- 📅 **Datetime Span Breakdown**: Displays earliest timestamp, latest timestamp, and overall date span in days.
- 📊 **Auto-Downsampled Interactive Visuals**:
  - Plotly dark-theme distribution histograms (automatically capped/sampled at 30k rows to keep notebooks snappy).
  - Categorical frequency bar charts for top categories.
- 🌐 **Universal Notebook Compatibility**: Renders seamlessly in VS Code Interactive Windows (`# %%`), JupyterLab, Classic Notebooks, and Google Colab.

---

## 🚀 Quick Start (In 3 Lines)

```python
import pandas as pd
from eda_tools import profile_data

df = pd.read_csv("your_dataset.csv")
profile_data(df)
```

---

## 💻 How to Use It Anywhere

### Option 1: Direct Pip Install from GitHub (Recommended)
You can install this tool directly into any virtual environment, Google Colab runtime, or Kaggle notebook:

```bash
pip install git+https://github.com/Hazardous9hub/EDA-Data-Profile-Tool.git
```

Then in Python:
```python
from EDA-Data-Profile-Tool import profile_data
```

---

### Option 2: 10-Second Quick Run in Google Colab / Kaggle
Don't want to install anything? Fetch and run it on the fly:

```python
# In your Colab notebook cell:
!curl -O https://raw.githubusercontent.com/Hazardous9hub/EDA-Data-Profile-Tool/main/eda_tools.py
from eda_tools import profile_data

# Run profile
profile_data(df)
```

---

### Option 3: Local Script / Drop-in File
Download [`eda_tools.py`](https://raw.githubusercontent.com/Hazardous9hub/EDA-Data-Profile-Tool/main/eda_tools.py) into your project root or `utils/` directory:

```python
from eda_tools import profile_data
```

---

## 🛠️ API & Parameter Reference

```python
profile_data(
    df: pd.DataFrame,
    target_num: str = None,
    target_cat: str = None,
    show_raw_info: bool = False
)
```

### Parameters

| Argument | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `df` | `pd.DataFrame` | *Required* | The dataset to analyze. |
| `target_num` | `str` | `None` | Specific numerical column to plot an interactive histogram for. If `None`, automatically picks the most relevant continuous variable. |
| `target_cat` | `str` | `None` | Specific categorical column to plot top frequencies for. If `None`, automatically picks an informative low-to-medium cardinality column. |
| `show_raw_info` | `bool` | `False` | When `True`, embeds a collapsible dropdown containing the raw output of `df.info()`. |

### Advanced Example

```python
# Target specific columns and inspect raw schema logs
profile_data(
    df=housing_df,
    target_num="SalePrice",
    target_cat="Neighborhood",
    show_raw_info=True
)
```

---

## 📦 Requirements

This tool avoids dependency bloat by using only standard data science stack packages:

- `pandas >= 1.3.0`
- `plotly >= 5.0.0`
- `ipython >= 7.0.0`

Install requirements:
```bash
pip install pandas plotly ipython
```

---


## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to open an issue or submit a pull request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
