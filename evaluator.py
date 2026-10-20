import json
import sqlite3
import uuid

from datetime import datetime
from openai import OpenAI


# Create the OpenAI client.
# This is what Python uses to communicate with the OpenAI API.
ai = OpenAI()


# Store the model name in one variable.
# If we want to test another model later, we only need to change it here.
model_name = "gpt-6-luna"


# Create one unique ID for this entire evaluator run.
# All 5 scenarios from this run will share the same run_id.
run_id = str(uuid.uuid4())


# Record when this evaluator run started.
created_at = datetime.now().isoformat()


# Open a connection to the SQLite database.
# If evaluations.db does not exist, SQLite will create it.
connection = sqlite3.connect("evaluations.db")


# Create a cursor.
# The cursor sends SQL commands to the database.
cursor = connection.cursor()


# Create the evaluations table if it does not already exist.
# id = unique number automatically assigned to each database row.
# category = Windows, Linux, Backup, Security, Network, etc.
# scenario = the IT problem we gave the AI.
# response = the AI's troubleshooting answer.
# model = which AI model generated the answer.
# run_id = groups all scenarios from one evaluator run together.
# created_at = records when the evaluator run happened.
cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    scenario TEXT,
    response TEXT,
    model TEXT,
    run_id TEXT,
    created_at TEXT
)
""")


# Open scenarios.json and load the IT test scenarios.
# json.load() converts the JSON data into Python lists and dictionaries.
with open("scenarios.json", "r") as file:
    scenarios = json.load(file)


# Create an empty list.
# Each completed AI test will be added to this list.
results = []


# Loop through every scenario in scenarios.json one at a time.
for item in scenarios:

    # Get the actual scenario text from the current dictionary.
    scenario = item["scenario"]


    # Send the scenario to the OpenAI API.
    # model = which AI model to use.
    # instructions = tells the AI what job it should perform.
    # input = the actual IT scenario being tested.
    response = ai.responses.create(
        model=model_name,
        instructions="You are an IT troubleshooting assistant. Give safe, practical troubleshooting steps.",
        input=scenario
    )


    # Build a Python dictionary containing the complete test result.
    # This will later be saved into evaluation_results.json.
    result = {
        "id": item["id"],
        "category": item["category"],
        "scenario": scenario,
        "expected_checks": item["expected_checks"],
        "model": model_name,
        "run_id": run_id,
        "created_at": created_at,
        "response": response.output_text
    }


    # Add this completed test result to the results list.
    results.append(result)


    # Save THIS scenario into the SQLite database.
    # Because this code is inside the for loop,
    # it will run once for every scenario.
    cursor.execute("""
    INSERT INTO evaluations (
        category,
        scenario,
        response,
        model,
        run_id,
        created_at
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        item["category"],
        scenario,
        response.output_text,
        model_name,
        run_id,
        created_at
    ))


    # Print the current scenario to the terminal.
    print("\nScenario:")
    print(scenario)


    # Print the current AI response to the terminal.
    print("\nAI Response:")
    print(response.output_text)


# Save all database changes after all scenarios have finished.
connection.commit()


# Close the database connection.
connection.close()


# Save all results from this run into a JSON file.
# "w" means write mode.
# indent=4 makes the JSON easier for humans to read.
# This file will be overwritten each time evaluator.py runs.
with open("evaluation_results.json", "w") as file:
    json.dump(results, file, indent=4)