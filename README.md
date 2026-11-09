# National Freight Transit Latency & Operational Efficiency for Nassau_Candy_Distributor
### An End-to-End Multi-Variate Analytics & Logistics Intelligence Framework

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)](https://streamlit.io/)

---

## 📌 Project Overview
This repository contains a comprehensive supply chain analytics project evaluating domestic freight transit performance, routing efficiency, and fulfillment channel reliability. The project combines **Exploratory Data Analysis (EDA)**, an academic research paper, a **Streamlit interactive analytics dashboard**, and strategic recommendations for government and corporate stakeholders.

---

## 🔍 Key Analytical Findings

1. **Multi-Modal Latency Distribution:** Fulfillment lead times exhibit severe right-skewness and tri-modal clustering, splitting network performance into baseline rapid dispatch (~910 days), standard operating peaks (~1280 days), and acute long-tail delay clusters (1600+ days).
2. **Spatial Bottlenecks:** State-level efficiency indexing ($E_r$) reveals a 100-point performance spread. While primary manufacturing corridors maintain high efficiency ($E_r \ge 74.0$), outlying regional destination hubs suffer from chronic intermodal transfer delays ($E_r \le 39.7$).
3. **Fulfillment Channel Invariance:** Cross-channel analysis proves that premium shipping tiers (Same Day, First Class) share identical median durations (~1270 days) and dispersion profiles with Standard Class, uncovering structural carrier neutralisation.

---

## 📂 Repository Structure

* **`NassauCandyDistributor.py`**: Live interactive Streamlit multi-page dashboard.
* **`Nassau_Candy_Distributor.ipynb`**: Jupyter Notebook containing the data preprocessing, cleaning pipeline, and statistical modeling.
* **`Figures/`**: Publication-grade 300 DPI visualizations embedded within the research paper.
* **`Research Paper.md`**: Formal 9-section academic research study.
* **`requirements.txt`**: Python dependencies required to run the codebase.

---

## 🛠️ Tech Stack & Development Tools

* **Analytics & Prototyping:** Jupyter Notebook (`.ipynb`) for exploratory data analysis, statistical modeling, and figure generation.
* **Application Development & Version Control:** PyCharm for building the Streamlit dashboard (`NassauCandyDistributor.py`) and managing local Git version control repositories.
* **Core Libraries:** Pandas, NumPy, Scikit-Learn, Seaborn, Matplotlib, Plotly, Streamlit.

---

## 🚀 How to Run the Project Locally

### 1. Clone the Repository
```bash
git clone [https://github.com/Hrithik3hl/Nassau_Candy_Distributor.git](https://github.com/Hrithik3hl/Nassau_Candy_Distributor.git)
cd Nassau_Candy_Distributor
