# TechNova HR Workforce Attrition Intelligence Platform

## Overview
A mid-size IT company (fictional: TechNova Solutions) with 4,000+ employees 
is facing 23% annual attrition — costing $8.5M in replacement and lost 
productivity. This platform identifies at-risk employees, uncovers root causes, 
and enables proactive HR intervention through data engineering, machine learning, 
and AI-generated insights.

## Architecture
Raw HR data stored in AWS S3 → ingested into Microsoft Fabric Lakehouse 
(Bronze/Silver Medallion layers) → transformed via PySpark → served through 
Fabric Data Warehouse (Gold layer Views) → visualized in Power BI Executive 
Dashboard with ML attrition risk scores and Claude AI-generated employee 
risk explanation cards.

## Key Features
- Synthetic HR dataset: 4,000 employees across 10 departments
- Medallion Architecture: Bronze → Silver → Gold
- 3 ML Models: K-Means Clustering, Decision Tree, Random Forest
- AI Risk Cards: Claude API generates plain-English explanation per employee
- Fabric Activator: automated alerts when attrition risk crosses threshold
- Power BI: drill-through dashboard with decomposition tree

## Tech Stack
| Layer | Technology |
|---|---|
| Raw Storage | AWS S3 |
| Ingestion | Microsoft Fabric Data Pipeline |
| Bronze/Silver | Fabric Lakehouse + PySpark |
| Gold | Fabric Data Warehouse + T-SQL Views |
| ML | Scikit-learn (K-Means, Decision Tree, Random Forest) |
| AI | Claude API (Anthropic) |
| BI | Power BI DirectQuery |
| Alerting | Microsoft Fabric Activator |
| Language | Python, PySpark, SQL, DAX |

## Dataset
Synthetic HR data generated using Python (Faker + NumPy) based on 
IBM HR Analytics dataset schema. Attrition patterns seeded using 
real-world risk factors including salary bands, overtime, promotion 
stagnation, and satisfaction scores.
