import json


with open("clients.json", "r") as file:
    clients = json.load(file)


def find_client_in_question(question):
    for client in clients:
        if client["name"].lower() in question.lower():
            return client

    return None


def get_devices(client):
    return client.get("devices", [])


def get_documents(client):
    return client.get("documents", [])


def understand_question_without_ai(question):
    question = question.lower()

    # Manually decide what counts as a device request
    if (
        "device" in question
        or "devices" in question
        or "firewall" in question
        or "switch" in question
        or "equipment" in question
    ):
        return "devices"

    # Manually decide what counts as a document request
    elif (
        "document" in question
        or "documents" in question
        or "documentation" in question
        or "docs" in question
        or "guide" in question
        or "kb" in question
    ):
        return "documents"

    else:
        return "unknown"


while True:
    question = input("\nNuvo NO-AI > ").strip()

    if question.lower() == "quit":
        print("Closing test.")
        break

    intent = understand_question_without_ai(question)
    client = find_client_in_question(question)

    if not client:
        print("Client not found.")
        continue

    if intent == "devices":
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
        print("I don't understand that request.")