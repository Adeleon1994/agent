import json
import sqlite3

from openai import OpenAI

ai = OpenAI()

connection = sqlite3.connect("evaluations.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    scenario TEXT,
    response TEXT
)
""")

with open("scenarios.json", "r") as file:
    scenarios = json.load(file)

results = []

for item in scenarios:
    scenario = item["scenario"]

    response = ai.responses.create(
        model="gpt-6-luna",
        instructions="You are an IT troubleshooting assistant. Give safe, practical troubleshooting steps.",
        input=scenario
    )

    result = {
        "id": item["id"],
        "category": item["category"],
        "scenario": scenario,
        "expected_checks": item["expected_checks"],
        "response": response.output_text
    }

    results.append(result)

    cursor.execute("""
    INSERT INTO evaluations (category, scenario, response)
    VALUES (?, ?, ?)
    """, (
        item["category"],
        scenario,
        response.output_text
    ))

    print("\nScenario:")
    print(scenario)

    print("\nAI Response:")
    print(response.output_text)

connection.commit()
connection.close()

with open("evaluation_results.json", "w") as file:
    json.dump(results, file, indent=4)