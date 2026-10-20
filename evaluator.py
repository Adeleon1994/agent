import json

from openai import OpenAI

ai = OpenAI()

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

    print("\nScenario:")
    print(scenario)

    print("\nAI Response:")
    print(response.output_text)

with open("evaluation_results.json", "w") as file:
    json.dump(results, file, indent=4)

