# dubai-rental-analysis




# ETL scheduling bu Windows task scheduler#
C:\Users\mzuba>schtasks /create /tn "RunDubaiETL" /tr "C:\Users\mzuba\Desktop\Final-project-BI-EUBS\dubai_rental_analysis\run_dubai_etl.bat" /sc daily /st 04:30
SUCCESS: The scheduled task "RunDubaiETL" has successfully been created.
