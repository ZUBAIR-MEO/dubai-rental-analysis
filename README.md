# DUBAI RENTAL ANALYSIS ETL PIPELINE
This project demonstrates a complete end-to-end ETL (Extract, Transform, Load) pipeline designed to collect, clean, store, and visualize real estate rental data in Dubai. It leverages open-source tools such as PostgreSQL, Python, Power BI, and Streamlit to provide actionable insights into Dubai's rental market.

# 🛠️ Project Overview
The ETL pipeline performs the following tasks:

*Data Source*
Raw rental data is sourced from an open dataset (CSV format) containing listings for Dubai's real estate market.

*Data Cleaning & Transformation*
Implemented within the single ETL script dubai_rental_data_pipeline.py using Python and Pandas to:

Extract data from CSV

Remove duplicates

Handle missing values

Filter and standardize column values

**Data Storage**
Cleaned data is stored in a PostgreSQL database with a well-defined schema.

*Workflow Scheduling*
The entire ETL process is automated with Windows Task Scheduler running a .bat file included in the repository:

Triggers daily execution of the pipeline

Runs automatically without user intervention

#  Email Notification:

Python-based email alert system:

Sends success/failure notifications using Gmail SMTP with SSL

Reads credentials securely from the .env configuration file


#  Data visualisation:

Power BI online dashboard offers deep insights into:

Pricing trends

Property types

Regional comparisons within Dubai

Additionally, a Streamlit dashboard is available for interactive web-based visualization, including predictive modeling of rental prices.


# 📁 Project Structure:
![image](https://github.com/user-attachments/assets/9f245c5d-7614-45f2-96c4-df60987fd6b8)


# ⚙️ Technologies used:

Python (Pandas, psycopg2, dotenv)

PostgreSQL

Windows Task Scheduler

Power BI (desktop & online)

Streamlit (interactive dashboard & predictive modeling)

SMTP (Gmail) for Email Notifications

# 🔐 Environment Configuration (.env)
![image](https://github.com/user-attachments/assets/a5bdba2d-cd00-4968-acc9-5ddb511f4013)



# 📧 Email Notification System

The main ETL script (dubai_rental_data_pipeline.py) includes a custom send_email_alert() function that:

Sends email notifications upon successful or failed pipeline execution.

Utilizes Gmail SMTP over SSL (port 465).

Reads all credentials securely from the .env file.

Provides timely updates without manual monitoring.

# ⏰ Task Automation (Windows task Scheduler):

The ETL pipeline is automated via Windows Task Scheduler by running the included batch file run_dubai_etl.bat. This batch file executes the ETL Python script with the proper environment setup.

_Example command to create the scheduled task (run in Command Prompt):_

"C:\Users\mzuba> schtasks /create /tn "RunDubaiETL" /tr "C:\Users\mzuba\Desktop\Final-project-BI-EUBS\dubai_rental_analysis\run_dubai_etl.bat" /sc daily /st 03:00"

_SUCCESS: The scheduled task "RunDubaiETL" has successfully been created.
_

# 📊 Dashboard Insights
Average rental prices by property type

Trends in price per square foot

Distribution of rents by number of bedrooms

Area-wise price comparison

**Power BI Online Dashboard**
Explore the live Power BI report here:
[Dubai Rental Market Dashboard](https://app.powerbi.com/groups/me/reports/e672daf5-9c9a-4f22-9c60-21eb59c02eaf/b3d063ecaf3c5e7e7ae6?experience=power-bi&bookmarkGuid=aa5db85f-ec2e-439a-85e0-1efef012e956)

**Streamlit Predictive Modeling**
For interactive exploration and rental price forecasting, visit the Streamlit app:
[Dubai Rental Predictive Model](https://zubair-meo-dubai-rental-analysis-app-stpcbn.streamlit.app/)

# 🚀 Getting Started

![image](https://github.com/user-attachments/assets/f293ce2b-73f8-4f59-997c-d701430f505d)

![image](https://github.com/user-attachments/assets/c4fa67dd-ac68-4873-9d85-5f58237f5acc)

