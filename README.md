# US Mortgage Underwriting & Condo Project Review Hub

An automated evaluation system using custom credit tiers, debt risk brackets, and property criteria. This Streamlit application runs a full simulated pipeline to analyze loan applicants and property compliance.

**🚀 Live Deployment:** [Launch Streamlit Web App](https://condo-underwriting-dashboard-dknhngmfzqcjticudtoyuo.streamlit.app/)

Created by **[srinivasta](https://github.com)**.

## ✨ Features
* **Interactive Parameters:** View core risk evaluation parameters using an expandable dashboard panel.
* **Live Configuration Sidebar:** Set custom sample sizes and dynamic condo active litigation probability percentages.
* **Underwriting Compliance Engine:** Evaluates applicants based on Credit Score, Debt-to-Income (DTI), and Condo HOA Reserves with lawsuit checks.
* **Visual Graphics Layer:** Displays dynamic compliance distributions using customized matplotlib pie charts.
* **Detailed Reports Table:** Filters out and targets approved clients who are officially clear to close.
* **Data Pipeline Export:** Download the entire simulated data sheet directly as a clean CSV format file.

## 🛠️ System Requirements
* Python 3.8 or higher
* Streamlit
* Pandas
* Numpy
* Matplotlib

## 🚀 Getting Started

### 1. Installation
Clone the repository or save the source file, then install the required dependencies:
```bash
pip install streamlit pandas numpy matplotlib
```

### 2. Run the Application Localy
Start the Streamlit dashboard server from your command line terminal:
```bash
streamlit run app.py
```

## 📊 Core Compliance Rules

### Credit Score Tiers
* **Excellent (800 - 900):** Instant Approval / Best Deals 🟢
* **Very Good (740 - 799):** Low Risk / Fast Approval 🟢
* **Good (670 - 739):** Standard Risk / Standard Rates 🟡
* **Fair (580 - 669):** High Risk / Strict Review 🟠
* **Poor (Below 580):** Severe Risk / Auto-Reject 🔴

### Debt-to-Income (DTI) Brackets
* **Excellent (Below 30.00%):** Low Debt Risk 🟢
* **Good (30.01% - 36.00%):** Manageable Debt 🟡
* **High Risk (36.01% - 43.00%):** Borderline Strain 🟠
* **Critical Danger (Over 43.00%):** Too Much Debt / Auto-Reject 🔴

### Condo Project Review Matrix
* **PASSED:** HOA Reserves $\ge$ 10% **AND** No Active Litigation 🟢
* **REJECTED:** HOA Reserves < 10% 🔴
* **REJECTED:** Dangerous Active Litigation Present 🔴
* **REJECTED:** Low Reserves & Active Lawsuit Combined 🔴

---
Developed by [srinivasta](https://github.com)
