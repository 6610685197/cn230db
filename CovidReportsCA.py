# Teepop Bambudpai 6610685197

import requests
import sqlite3

# Pull data from an API
url = "https://api.covid19tracker.ca/reports/province/on"
response = requests.get(url)
responseData = response.json()
data = responseData["data"]

# print(response)
# print(responseData)

# Create Database
conn = sqlite3.connect("CovidReportsCA.db")
cur = conn.cursor()

# cur.execute('''
#     DROP TABLE covid_reports
#             ''')

# Create Table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS covid_reports (
        date TEXT,
        change_cases INTEGER,
        change_fatalities INTEGER,
        change_tests INTEGER,
        change_hospitalizations INTEGER,
        change_criticals INTEGER,
        change_recoveries INTEGER,
        change_vaccinations INTEGER,
        change_vaccinated INTEGER,
        change_boosters_1 INTEGER,
        change_boosters_2 INTEGER,
        change_vaccines_distributed INTEGER,
        total_cases INTEGER,
        total_fatalities INTEGER,
        total_tests INTEGER
        total_hospitalizations INTEGER,
        total_criticals INTEGER,
        total_recoveries INTEGER,
        total_vaccinations INTEGER,
        total_boosters_1 INTEGER,
        total_boosters_2 INTEGER,
        total_vaccines_distributed INTEGER
    )
"""
)

# Insert data into Table
for report in data:
    cur.execute(
        """
        INSERT INTO covid_reports 
        (date, change_cases,
        change_fatalities,
        change_tests,
        change_hospitalizations,
        change_criticals,
        change_recoveries,
        change_vaccinations,
        change_vaccinated,
        change_boosters_1,
        change_boosters_2,
        change_vaccines_distributed,
        total_cases,
        total_fatalities,
        total_tests,
        total_criticals,
        total_recoveries,
        total_vaccinations,
        total_boosters_1,
        total_boosters_2,
        total_vaccines_distributed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?)
    """,
        (
            report.get("date"),
            report.get("change_cases"),
            report.get("change_fatalities"),
            report.get("change_tests"),
            report.get("change_hospitalizations"),
            report.get("change_criticals"),
            report.get("change_recoveries"),
            report.get("change_vaccinations"),
            report.get("change_vaccinated"),
            report.get("change_boosters_1"),
            report.get("change_boosters_2"),
            report.get("change_vaccines_distributed"),
            report.get("total_cases"),
            report.get("total_fatalities"),
            report.get("total_tests"),
            report.get("total_criticals"),
            report.get("total_recoveries"),
            report.get("total_vaccinations"),
            report.get("total_boosters_1"),
            report.get("total_boosters_2"),
            report.get("total_vaccines_distributed"),
        ),
    )
    conn.commit()

print("Average cases per day from Ontario, California")
for row in cur.execute("SELECT AVG(change_cases) FROM covid_reports"):
    print(round(row[0]), "cases")

print("Total cases from Ontario, California")
for row in cur.execute(
    "SELECT date, total_cases FROM covid_reports ORDER BY date DESC LIMIT 1"
):
    print(row[1], "cases")

conn.close()
