# 🚀 Monday.com Business Intelligence Agent

## 📌 Overview

This project is a founder-level Business Intelligence (BI) agent built on top of monday.com boards.

It dynamically connects to:

- 📊 Deals Board (Sales Pipeline)
- 🏗 Work Orders Board (Execution & Revenue)

The agent transforms messy operational data into structured, executive-ready insights through a conversational interface.

Hosted via Streamlit Cloud.

---

## 🎯 Problem Statement

Founders and executives need fast, reliable answers to questions like:

- How is our pipeline looking?
- Are we overly dependent on one sector?
- What is our revenue this quarter?
- How diversified is our exposure?
- Prepare a leadership update.

Business data is messy and spread across multiple boards.

This system solves that problem.

---

## 🏗 Architecture Overview

### 1️⃣ Data Layer
- monday.com API (Read-only integration)
- Dynamic board fetching (no CSV hardcoding)

### 2️⃣ Processing Layer
- Pandas for aggregation
- Automatic detection of:
  - Sector columns
  - Revenue columns
  - Month columns
- Data normalization for messy formats

### 3️⃣ Intelligence Layer
Rule-based NLP routing for:
- Pipeline queries
- Sector dominance
- Concentration risk
- Revenue breakdown
- Month-wise revenue
- Quarter filtering
- Leadership updates

### 4️⃣ Presentation Layer
- Streamlit conversational UI
- Executive formatting
- Sector visualization (bar chart)

---

## 📊 Features

### 🔹 Pipeline Intelligence
- Total deal count
- Total pipeline value
- Sector dominance detection
- Concentration risk calculation

### 🔹 Revenue Intelligence
- Revenue summary
- Sector-wise revenue breakdown
- Month-wise revenue breakdown
- Quarter filtering (Q1–Q4)

### 🔹 Executive Reporting
- Leadership update generator
- Board-level snapshot formatting

### 🔹 Data Resilience
- Handles inconsistent month names
- Handles missing numeric fields
- Safe aggregation with fallbacks

---

## 🛠 Tech Stack

- Python
- Streamlit
- Pandas
- Matplotlib
- monday.com API

---

## 🔐 Security

- API tokens stored securely in Streamlit Secrets
- No hardcoded credentials
- Read-only board access

---

## 🚀 Deployment

Hosted on Streamlit Cloud.

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py