import json

from openai import OpenAI

ai = OpenAI()

scenario = "A Windows Server C: drive is 98% full."

response = ai.responses.create(
    model="gpt-6-luna",
    instructions="You are an IT troubleshooting assistant. Give safe, practical troubleshooting steps.",
    input=scenario
)

result = {
    "scenario": scenario,
    "response": response.output_text
}


with open("evaluation_results.json", "w") as file:
    json.dump(result, file, indent=4)


print(response.output_text)

