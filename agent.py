import json


def load_clients():
    try:
        with open("clients.json", "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print("Could not find clients.json")
        return []

    except json.JSONDecodeError:
        print("clients.json contains invalid JSON")
        return []


clients = load_clients()


def find_clients(client_name):
    matches = []

    for client in clients:
        if client_name.strip().lower() in client["name"].lower():
            matches.append(client)

    return matches

def find_client_in_question(question):
    for client in clients:
        if client["name"].lower() in question.lower():
            return client

    return None

def get_devices(client):
    return client.get("devices", [])


def get_documents(client):
    return client.get("documents", [])


while True:
    question = input("\nNuvo Agent > ").strip()

    if question.lower() == "quit":
        print("Closing Nuvo Agent.")
        break

    client = find_client_in_question(question)

    if "devices" in question.lower():

        if client:
            devices = get_devices(client)

            print(f"\nDevices for {client['name']}:")

            for device in devices:
                print(f"{device['name']} - {device['type']} - {device['ip']}")

        else:
            print("I know you're asking about devices, but I couldn't find the client.")

    elif "documents" in question.lower():

        if client:
            documents = get_documents(client)

            print(f"\nDocuments for {client['name']}:")

            for document in documents:
                print(document["title"])

        else:
            print("I know you're asking about documents, but I couldn't find the client.")

    else:
        print("I don't understand the request yet.")