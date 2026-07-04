# TechNova HR Workforce Attrition Intelligence Platform

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Microsoft%20Fabric-purple)
![Power Bi](https://img.shields.io/badge/Query-SQL-blue)
![Power Bi](https://img.shields.io/badge/Visualization-PowerBI-yellow)
![ML](https://img.shields.io/badge/ML-Scikit--learn-orange)

## Business Problem

TechNova Solutions, a mid-size IT company with 4,000+ employees, is experiencing 
23% annual attrition — nearly 3× the IT industry benchmark of 13-15%. This 
translates to approximately $8.5M in annual replacement and productivity costs.

This platform was built to answer three critical questions:
- **Who** is at risk of leaving in the next 6 months?
- **Why** are they leaving — what are the root causes?
- **What** should HR do about it — specific, timely interventions?

---

## Solution Architecture
# HR Workforce Analytics Architecture

```text
AWS S3 (Raw HR Data)
        │
        ▼
Microsoft Fabric Data Pipeline
(Fan-Out — 4 Parallel Copy Activities)
        │
        ▼
Fabric Lakehouse — Bronze Layer
(Raw Delta Files)
        │
        ▼
PySpark Notebook — Silver Transformation
(Cleaned, Typed, Joined Master Table)
        │
        ▼
Fabric Data Warehouse — Gold Layer
(Business-Ready T-SQL Views)
        │
        ▼
┌─────────────────────────────────────────────┐
│      Power BI Dashboard (DirectQuery)       │
│                                             │
│  • Page 1: Executive Summary                │
│  • Page 2: Risk Intelligence                │
│  • Page 3: People Analytics Deep Dive       │
│  • Page 4: AI Risk Card (Drill-through)     │
└─────────────────────────────────────────────┘

                     +
                     │
                     ▼
Google Gemini API
(AI-Generated HR Intervention Recommendations)
```
---

## Key Features

| Feature | Description |
|---|---|
| **Medallion Architecture** | Bronze → Silver → Gold separation of concerns |
| **Fan-Out Pipeline** | 4 parallel ingestion activities from AWS S3 |
| **Weekly Scheduling** | Automated pipeline runs every Sunday at 6AM |
| **3 ML Models** | K-Means Clustering, Decision Tree, Random Forest |
| **AI Risk Cards** | Gemini API generates plain-English HR recommendations per employee |
| **Drill-Through** | Click any employee in Page 2 → AI Risk Card on Page 4 |
| **Employee Search** | Searchable by Name or EmployeeID — scales to 10K+ employees |
| **Conditional Formatting** | Risk-level color coding across all visuals |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Raw Storage | AWS S3 |
| Ingestion | Microsoft Fabric Data Pipeline |
| Bronze / Silver | Fabric Lakehouse + PySpark |
| Gold | Fabric Data Warehouse + T-SQL Views |
| Machine Learning | Scikit-learn (K-Means, Decision Tree, Random Forest) |
| AI Integration | Google Gemini API |
| Business Intelligence | Power BI (DirectQuery, DAX, Drill-through) |
| Language | Python, PySpark, T-SQL, DAX |

---

## Machine Learning Results

| Model | Type | Accuracy | Recall | Purpose |
|---|---|---|---|---|
| K-Means (K=4) | Unsupervised | N/A | N/A | Employee segmentation |
| Decision Tree | Supervised | 57.9% | 28.5% | Interpretable baseline |
| Random Forest | Supervised | 58.1% | **49.8%** | Production predictor |

**Key finding:** Random Forest improved recall by 74.7% over Decision Tree 
by combining 200 trees with balanced class weighting — catching nearly 
half of all employees who would actually leave.

**Top attrition predictors (Random Forest feature importance):**
1. Monthly Income (10.3%)
2. Distance From Home (9.2%)
3. Age (8.4%)
4. Average Hours Per Day (8.2%)
5. Years Since Last Promotion (7.6%)

---

## Key Business Insights

- Attrition rate of **41.6%** — nearly 3× IT industry benchmark
- **Stagnation, not salary**, is the root cause among high earners:
  employees earning above ₹55K with 4+ years without promotion 
  show the highest attrition regardless of compensation level
- **Software Engineering** shows classic burnout profile: 53% overtime 
  + 45% stagnation rate despite competitive salaries
- **IT Infrastructure** presents most critical risk: 55% low satisfaction 
  + promotion gaps of up to 7 years
- **Environment Satisfaction** alone significantly impacts attrition even 
  when controlling for tenure and salary — revealed through K-Means 
  cluster comparison (Content Newcomers vs Disengaged Newcomers)

---

## Employee Segments (K-Means Clustering)

| Cluster | Size | Attrition Rate | Profile |
|---|---|---|---|
| Stagnant Mid-Career | 1,111 | **46.4%** | Moderate salary, 6+ yrs, highest promotion gap |
| Senior Veterans | 544 | 43.4% | Highest salary, 12+ yrs, burnout-driven |
| Disengaged Newcomers | 1,183 | 40.0% | Low tenure, lowest environment satisfaction |
| Content Newcomers | 1,162 | **37.9%** | Low tenure, highest environment satisfaction |

---

## Dashboard Screenshots

### Page 1 — Executive Summary
<img width="1280" height="718" alt="image" src="https://github.com/user-attachments/assets/3a0f04ca-5059-4eb7-878e-c781981752fd" />



### Page 2 — Risk Intelligence
<img width="1285" height="721" alt="image" src="https://github.com/user-attachments/assets/2de41819-f23b-4efb-98cc-cb6a5d53ca76" />

### Page 3 — People Analytics Deep Dive
<img width="1280" height="724" alt="image" src="https://github.com/user-attachments/assets/8d627364-f8cd-4210-945d-fa6710a8c9c0" />


### Page 4 — AI Risk Card
<img width="1284" height="715" alt="image" src="https://github.com/user-attachments/assets/f3b61ff1-b443-41b0-97d7-f2f2b5f2dd94" />

---

## Video Demonstration

🎥 **Dashboard walkthrough video — Coming Soon**

*Full demonstration of drill-through navigation, AI risk card generation, 
employee search, and slicer interactions across all 4 pages.*

---

## Repository Structure
```text
TechNova-HR-Attrition-Intelligence-Platform/
│
├── dataset/
│   └── dataset_generator.py          # Synthetic HR data generation + S3 upload
│
├── notebooks/
│   ├── NB_Silver_Transformation.ipynb   # PySpark Bronze → Silver transformation
│   ├── NB_ML_Attrition_Models.ipynb     # K-Means, Decision Tree, Random Forest
│   └── NB_AI_Risk_Cards.ipynb           # Gemini API risk card generation
│
├── sql/
│   ├── vw_HR_Master.sql              # Gold layer master view (all columns + ML)
│   ├── Silver_Master_Query.sql       # Silver transformation SQL reference
│   └── SQL_Warmups.sql               # Practice queries used during development
│
├── screenshots/
│   ├── page1_executive_summary.png
│   ├── page2_risk_intelligence.png
│   ├── page3_people_analytics.png
│   └── page4_ai_risk_card.png
│
├── architecture/
│   └── architecture_diagram.png      # End-to-end architecture diagram
│
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## Dataset

Synthetic HR data generated using Python (Faker + NumPy) based on IBM HR Analytics 
dataset schema. 4,000 employee records across 10 departments with realistic:
- Salary banding by department and job level
- Attrition patterns seeded using real-world risk factors
- Satisfaction scores, overtime patterns, and promotion gaps

---

## Author

**Arghyajyoti Samui**  
Analyst @ HCLTech | Transitioning to Data Analytics & Analytics Engineering  
[LinkedIn](https://linkedin.com/in/arghyajyoti-samui) · 
[GitHub](https://github.com/Arghyajyoti007)
