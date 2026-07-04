import boto3
import os
import pandas as pd
import numpy as np
from faker import Faker
from dotenv import load_dotenv
import io
import random

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────
load_dotenv()
fake = Faker('en_IN')
np.random.seed(42)  # Ensures reproducibility — same data every run
random.seed(42)

TOTAL_EMPLOYEES = 4000
BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

# ─────────────────────────────────────────
# MASTER REFERENCE DATA
# ─────────────────────────────────────────
DEPARTMENT_ROLES = {
    "Software Engineering": [
        "Software Engineer", "Senior Software Engineer",
        "Tech Lead", "Engineering Manager"
    ],
    "Data & Analytics": [
        "Data Analyst", "BI Developer",
        "Data Engineer", "Analytics Manager"
    ],
    "Human Resources": [
        "HR Executive", "HR Specialist",
        "HR Business Partner", "HR Manager"
    ],
    "Sales & Business Development": [
        "Sales Executive", "Senior Sales Executive",
        "Sales Manager", "Business Development Manager"
    ],
    "Finance": [
        "Finance Analyst", "Senior Finance Analyst",
        "Finance Controller", "Finance Manager"
    ],
    "IT Infrastructure": [
        "System Administrator", "Network Engineer",
        "Infrastructure Lead", "IT Manager"
    ],
    "Legal & Compliance": [
        "Legal Executive", "Compliance Analyst",
        "Senior Legal Counsel", "Legal Manager"
    ],
    "Operations & Admin": [
        "Operations Executive", "Senior Operations Executive",
        "Operations Lead", "Operations Manager"
    ],
    "Marketing & Communications": [
        "Marketing Executive", "Content Strategist",
        "Marketing Lead", "Marketing Manager"
    ],
    "Customer Success": [
        "Customer Success Executive", "Senior CSE",
        "Customer Success Lead", "Customer Success Manager"
    ]
}

# Salary bands: Department → [L1, L2, L3, L4] ranges
# Each level = (min_salary, max_salary) in INR monthly
SALARY_BANDS = {
    "Software Engineering":          [(45000,65000),(65000,110000),(110000,180000),(180000,300000)],
    "Data & Analytics":              [(50000,75000),(75000,130000),(130000,200000),(200000,320000)],
    "Human Resources":               [(30000,50000),(50000,80000),(80000,130000),(130000,200000)],
    "Sales & Business Development":  [(25000,40000),(40000,70000),(70000,120000),(120000,200000)],
    "Finance":                       [(35000,55000),(55000,90000),(90000,150000),(150000,250000)],
    "IT Infrastructure":             [(30000,50000),(50000,85000),(85000,140000),(140000,220000)],
    "Legal & Compliance":            [(40000,65000),(65000,100000),(100000,160000),(160000,260000)],
    "Operations & Admin":            [(25000,40000),(40000,65000),(65000,110000),(110000,180000)],
    "Marketing & Communications":    [(28000,45000),(45000,75000),(75000,120000),(120000,190000)],
    "Customer Success":              [(25000,42000),(42000,70000),(70000,115000),(115000,185000)]
}

# Job level distribution — most employees are L1/L2
# Realistic org pyramid shape
LEVEL_WEIGHTS = [0.40, 0.35, 0.17, 0.08]  # 40% L1, 35% L2, 17% L3, 8% L4


# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def assign_job_level():
    """Assign job level based on org pyramid weights"""
    return np.random.choice([1, 2, 3, 4], p=LEVEL_WEIGHTS)


def assign_salary(department, job_level):
    """
    Assign salary based on department and job level.
    This is conditional distribution — salary depends on other columns.
    Much more realistic than random salary assignment.
    """
    band = SALARY_BANDS[department][job_level - 1]
    return random.randint(band[0], band[1])


def assign_years_at_company(job_level):
    """
    Senior employees naturally have more years at company.
    L1: 0-3 years, L2: 2-7 years, L3: 5-12 years, L4: 8-20 years
    """
    ranges = {1: (0,3), 2: (2,7), 3: (5,12), 4: (8,20)}
    r = ranges[job_level]
    return random.randint(r[0], r[1])


def calculate_attrition(salary, dept, job_level, overtime,
                         job_satisfaction, work_life_balance,
                         years_since_promotion, num_companies):
    """
    Attrition is NOT random — it follows real-world patterns.
    Each negative factor increases attrition probability.
    This seeds meaningful patterns for our ML model to learn.
    """
    # Start with base attrition rate for IT industry
    base_risk = 0.15

    # Salary below band minimum increases risk significantly
    band_min = SALARY_BANDS[dept][job_level - 1][0]
    if salary < band_min * 1.1:
        base_risk += 0.15

    # Overtime is one of the strongest attrition signals
    if overtime == "Yes":
        base_risk += 0.12

    # Low job satisfaction
    if job_satisfaction <= 2:
        base_risk += 0.10

    # Poor work life balance
    if work_life_balance <= 2:
        base_risk += 0.08

    # Stagnation — no promotion in 3+ years
    if years_since_promotion >= 3:
        base_risk += 0.10

    # Job hopper pattern — likely to hop again
    if num_companies >= 4:
        base_risk += 0.07

    # Cap at 85% — even unhappy employees sometimes stay
    base_risk = min(base_risk, 0.85)

    return "Yes" if random.random() < base_risk else "No"


def upload_to_s3(df, folder, filename):
    """
    Upload dataframe directly to S3 as CSV.
    No need to save locally first — we use in-memory buffer.
    This is more efficient for large datasets.
    """
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3_key = f"{folder}/{filename}"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
        Body=csv_buffer.getvalue()
    )
    print(f"✅ Uploaded: s3://{BUCKET_NAME}/{s3_key} "
          f"({len(df)} rows)")


# ─────────────────────────────────────────
# DATA GENERATION
# ─────────────────────────────────────────
def generate_all_data():
    print(f"🚀 Generating {TOTAL_EMPLOYEES} employee records...")
    print(f"📦 Target bucket: {BUCKET_NAME}\n")

    # Lists to collect all records
    employees_data    = []
    performance_data  = []
    satisfaction_data = []
    attendance_data   = []

    departments = list(DEPARTMENT_ROLES.keys())

    for emp_id in range(1001, 1001 + TOTAL_EMPLOYEES):

        # ── Core attributes ──────────────────
        dept       = random.choice(departments)
        job_level  = assign_job_level()
        job_role   = DEPARTMENT_ROLES[dept][job_level - 1]
        age        = random.randint(22, 58)
        experience = assign_years_at_company(job_level)
        salary     = assign_salary(dept, job_level)

        # ── Satisfaction scores (1-4 scale) ──
        job_sat    = random.randint(1, 4)
        wlb        = random.randint(1, 4)
        rel_sat    = random.randint(1, 4)
        env_sat    = random.randint(1, 4)
        job_inv    = random.randint(1, 4)

        # ── Performance attributes ────────────
        overtime           = random.choice(["Yes", "No"])
        perf_rating        = random.randint(1, 4)
        training_times     = random.randint(0, 6)
        years_in_role      = min(random.randint(0, 5), experience)
        years_since_promo  = min(random.randint(0, 7), experience)
        total_working_yrs  = experience + random.randint(0, 5)
        num_companies      = random.randint(1, 8)

        # ── Attrition — pattern based ─────────
        attrition = calculate_attrition(
            salary, dept, job_level, overtime,
            job_sat, wlb, years_since_promo, num_companies
        )

        # ── Attendance ────────────────────────
        avg_hours      = round(random.uniform(7.5, 11.5), 1)
        avg_laptop_hrs = round(avg_hours - random.uniform(0.5, 1.5), 1)
        leave_days     = random.randint(0, 24)
        absent_days    = random.randint(0, 15)
        travel_freq    = random.choice([
            "Non-Travel", "Travel_Rarely", "Travel_Frequently"
        ])

        # ── Build each table row ──────────────
        employees_data.append({
            "EmployeeID":          emp_id,
            "Name":                fake.name(),
            "Age":                 age,
            "Gender":              random.choice(["Male", "Female"]),
            "MaritalStatus":       random.choice(["Single","Married","Divorced"]),
            "Education":           random.randint(1, 5),
            "EducationField":      random.choice([
                "Life Sciences","Medical","Marketing",
                "Technical Degree","Human Resources","Other"
            ]),
            "Department":          dept,
            "JobRole":             job_role,
            "JobLevel":            job_level,
            "MonthlyIncome":       salary,
            "YearsAtCompany":      experience,
            "NumCompaniesWorked":  num_companies,
            "DistanceFromHome":    random.randint(1, 60),
            "Attrition":           attrition
        })

        performance_data.append({
            "EmployeeID":              emp_id,
            "PerformanceRating":       perf_rating,
            "OverTime":                overtime,
            "TrainingTimesLastYear":   training_times,
            "YearsInCurrentRole":      years_in_role,
            "YearsSinceLastPromotion": years_since_promo,
            "TotalWorkingYears":       total_working_yrs
        })

        satisfaction_data.append({
            "EmployeeID":               emp_id,
            "JobSatisfaction":          job_sat,
            "WorkLifeBalance":          wlb,
            "RelationshipSatisfaction": rel_sat,
            "EnvironmentSatisfaction":  env_sat,
            "JobInvolvement":           job_inv,
            "StockOptionLevel":         random.randint(0, 3)
        })

        attendance_data.append({
            "EmployeeID":             emp_id,
            "AvgHoursPerDay":         avg_hours,
            "AvgLaptopActiveHours":   avg_laptop_hrs,
            "LeaveDaysTaken":         leave_days,
            "AbsentDaysLastYear":     absent_days,
            "BusinessTravelFrequency": travel_freq
        })

    # ── Convert to DataFrames ─────────────
    df_employees    = pd.DataFrame(employees_data)
    df_performance  = pd.DataFrame(performance_data)
    df_satisfaction = pd.DataFrame(satisfaction_data)
    df_attendance   = pd.DataFrame(attendance_data)

    # ── Quick validation before upload ────
    print("📊 Data Summary:")
    print(f"   Total employees : {len(df_employees)}")
    attrition_rate = (
        df_employees['Attrition'].value_counts()['Yes'] /
        len(df_employees) * 100
    )
    print(f"   Attrition rate  : {attrition_rate:.1f}%")
    print(f"   Departments     : "
          f"{df_employees['Department'].nunique()}")
    print(f"   Avg salary (INR): "
          f"{df_employees['MonthlyIncome'].mean():,.0f}\n")

    # ── Upload all 4 files to S3 ──────────
    print("📤 Uploading to S3...")
    upload_to_s3(df_employees,   "employees",   "employees.csv")
    upload_to_s3(df_performance, "performance", "performance.csv")
    upload_to_s3(df_satisfaction,"satisfaction","satisfaction.csv")
    upload_to_s3(df_attendance,  "attendance",  "attendance.csv")

    print("\n🎉 All files uploaded successfully!")
    print(f"🪣 Bucket: s3://{BUCKET_NAME}/")


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────
if __name__ == "__main__":
    generate_all_data()
