from openai import OpenAI

ai = OpenAI()

while True:
    question = input("\nTech > ")

    if question.strip().lower() == "quit":
        print("Closing troubleshooting test.")
        break

    response = ai.responses.create(
        model="gpt-6-luna",

        instructions="""
You are an IT troubleshooting assistant.

Help diagnose Windows, Linux, networking, backups,
security alerts, and general infrastructure problems.

Explain what you think is happening.
Recommend safe troubleshooting steps.
Explain why you recommend each step.
Ask for more information when needed.

Do not invent facts about a customer's environment.
Do not claim you checked a system unless information
or a tool result was actually provided.
Stay within IT troubleshooting.
""",

        input=question
    )

    print("\nNuvo AI:")
    print(response.output_text)