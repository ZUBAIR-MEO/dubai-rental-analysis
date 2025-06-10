#Dubai Rental Analysis ETL Pipeline
This project demonstrates a complete end-to-end ETL (Extract, Transform, Load) pipeline designed to collect, clean, store, and visualize real estate rental data in Dubai. It leverages open-source tools such as PostgreSQL, Python, Power BI, and Streamlit to provide actionable insights into Dubai's rental market.

🛠️ Project Overview
The ETL pipeline performs the following tasks:

Data Source
Raw rental data is sourced from an open dataset (CSV format) containing listings for Dubai's real estate market.

Data Cleaning & Transformation
Implemented within the single ETL script dubai_rental_data_pipeline.py using Python and Pandas to:

Extract data from CSV

Remove duplicates

Handle missing values

Filter and standardize column values

Data Storage
Cleaned data is stored in a PostgreSQL database with a well-defined schema.

Workflow Scheduling
The entire ETL process is automated with Windows Task Scheduler running a .bat file included in the repository:

Triggers daily execution of the pipeline

Runs automatically without user intervention

Email Notifications
Python-based email alert system:

Sends success/failure notifications using Gmail SMTP with SSL

Reads credentials securely from the .env configuration file

Data Visualization
Power BI online dashboard offers deep insights into:

Pricing trends

Property types

Regional comparisons within Dubai

Additionally, a Streamlit dashboard is available for interactive web-based visualization, including predictive modeling of rental prices.

📁 Project Structure
bash
Copy
Edit
Final-project-BI-EUBS/
│
├── dubai_rental_analysis/
│   ├── dubai_rental_data_pipeline.py     # Main ETL script (extract, transform, load) with email alert integration
│   ├── run_dubai_etl.bat                  # Batch file to run ETL script (used by Task Scheduler)
│   ├── data/
│   │   ├── rents-2025-05-30.csv          # Raw rental data CSV
│   │   └── Dubai_rents_May_2025_cleaned.csv  # Cleaned data CSV
│   ├── sql/
│   │   └── create_tables.sql             # PostgreSQL schema creation script
│
├── powerbi_dashboard/
│   └── dubai_rent_dashboard.pbix         # Power BI desktop dashboard file (optional)
│
├── .env                                   # Configuration file for environment variables
├── requirements.txt                       # Python dependencies
└── README.md
⚙️ Technologies Used
Python (Pandas, psycopg2, dotenv)

PostgreSQL

Windows Task Scheduler

Power BI (desktop & online)

Streamlit (interactive dashboard & predictive modeling)

SMTP (Gmail) for Email Notifications

🔐 Environment Configuration (.env)
ini
Copy
Edit
# PostgreSQL Database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres

# Email Notifications
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECEIVER=receiver@example.com
EMAIL_PASSWORD=your_app_password

# File Paths
DATA_FILE_PATH=./Dubai_rents_May_2025_cleaned.csv
📧 Email Notification System
The main ETL script (dubai_rental_data_pipeline.py) includes a custom send_email_alert() function that:

Sends email notifications upon successful or failed pipeline execution.

Utilizes Gmail SMTP over SSL (port 465).

Reads all credentials securely from the .env file.

Provides timely updates without manual monitoring.

⏰ Task Automation with Windows Task Scheduler
The ETL pipeline is automated via Windows Task Scheduler by running the included batch file run_dubai_etl.bat. This batch file executes the ETL Python script with the proper environment setup.

Example command to create the scheduled task (run in Command Prompt):

cmd
Copy
Edit
C:\Users\mzuba> schtasks /create /tn "RunDubaiETL" /tr "C:\Users\mzuba\Desktop\Final-project-BI-EUBS\dubai_rental_analysis\run_dubai_etl.bat" /sc daily /st 04:30

SUCCESS: The scheduled task "RunDubaiETL" has successfully been created.
Make sure that:

The .bat file path is correct.

The .env file and dependencies are properly configured.

📊 Dashboard Insights
Average rental prices by property type

Trends in price per square foot

Distribution of rents by number of bedrooms

Area-wise price comparison

Power BI Online Dashboard
Explore the live Power BI report here:
Dubai Rental Market Dashboard

Streamlit Predictive Modeling
For interactive exploration and rental price forecasting, visit the Streamlit app:
Dubai Rental Predictive Model

🚀 Getting Started
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/Final-project-BI-EUBS.git
cd Final-project-BI-EUBS
Create and activate a virtual environment:

bash
Copy
Edit
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
Install required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
Create and configure your .env file based on the template above.

Run the ETL pipeline manually or via the batch file:

bash
Copy
Edit
python dubai_rental_analysis/dubai_rental_data_pipeline.py
# or
dubai_rental_analysis\run_dubai_etl.bat
🧱 Optional Enhancements
Built-in email alert system (already included)

Web dashboard (Streamlit) for real-time data interaction and predictive modeling

Advanced predictive modeling for rental price forecasting

📌 License
This project is open-source and available under the MIT License.
