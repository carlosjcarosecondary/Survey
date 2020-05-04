Objective:
The purpose of this program is to collect the response from all users across 3 surveys.
Eacj survey has a determined number of questions

Database connection:
- Database: SQL Server
- Database name: ABRAXAS-WINDOWS

Libraries required:
- pyodbc: to establish connection with the database
- csv: to create a CSV file to save the results

Error management - codes:
- 101: connection with the database could not be established
- 102: query could not be executed due to a connection error
- 201: query could not be executed due to a query error
- 301: CSV file could not be created 

Output:
The program should produced a CSV file titled: 'survey_report.csv' (approx file size: 60,773KB). If the answer column has a '-1' is because the user did not respond that question.