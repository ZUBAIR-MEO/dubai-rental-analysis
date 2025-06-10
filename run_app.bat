    @echo off
    cd /d "C:\Users\mzuba\Desktop\Final-project-BI-EUBS\dubai_rental_analysis"
call venv\Scripts\activate.bat
streamlit run models/App.py
deactivate