import json
from openai import OpenAI

ai = OpenAI()


with open("clients.json", "r") as file:
    clients = json.load(file)


client_names = []

for client in clients:
    client_names.append(client["name"])


def understand_question(question):
    response = ai.responses.create(
        model="gpt-6-luna",

        instructions=f"""
You are the request router for Nuvo Agent.

Valid clients: {client_names}

Valid intents:
devices
documents
unknown

Identify the client and intent from the user's question.

If the user asks about every client or all clients,
set client=all.

Reply exactly like this:
intent=devices; client=Nubo

Examples:

"show me Nubo devices"
intent=devices; client=Nubo

"show me all client devices"
intent=devices; client=all

"show me Cleverspin documentation"
intent=documents; client=Cleverspin

If you cannot identify something, use unknown.
""",

        input=question
    )

    return response.output_text


def parse_ai_response(response_text):
    parts = response_text.split(";")

    intent = parts[0].split("=")[1].strip()
    client_name = parts[1].split("=")[1].strip()

    return intent, client_name


def find_client_by_name(client_name):
    for client in clients:
        if client["name"].lower() == client_name.lower():
            return client

    return None


def get_devices(client):
    return client.get("devices", [])


def get_documents(client):
    return client.get("documents", [])

def get_devices_by_client(client_name):
    client = find_client_by_name(client_name)

    if not client:
        return "Client not found."

    return client.get("devices", [])

while True:
    question = input("\nNuvo AI > ")

    if question.strip().lower() == "quit":
        print("Closing AI test.")
        break

    result = understand_question(question)

    intent, client_name = parse_ai_response(result)

    if client_name.lower() == "all":

        if intent == "devices":
            for client in clients:
                print(f"\nDevices for {client['name']}:")

                devices = get_devices(client)

                for device in devices:
                    print(f"{device['name']} - {device['type']} - {device['ip']}")

        elif intent == "documents":
            for client in clients:
                print(f"\nDocuments for {client['name']}:")

                documents = get_documents(client)

                for document in documents:
                    print(document["title"])

    else:
        client = find_client_by_name(client_name)

        if not client:
            print("Client not found.")

        elif intent == "devices":
            devices = get_devices(client)

            print(f"\nDevices for {client['name']}:")

            for device in devices:
                print(f"{device['name']} - {device['type']} - {device['ip']}")

        elif intent == "documents":
            documents = get_documents(client)

            print(f"\nDocuments for {client['name']}:")

            for document in documents:
                print(document["title"])

        else:
            print("I don't know how to handle that request yet.")