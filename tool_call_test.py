import json
from openai import OpenAI

ai = OpenAI()


with open("clients.json", "r") as file:
    clients = json.load(file)


def find_client_by_name(client_name):
    for client in clients:
        if client["name"].lower() == client_name.lower():
            return client

    return None


def get_devices_by_client(client_name):
    client = find_client_by_name(client_name)

    if not client:
        return {"error": "Client not found"}

    return client.get("devices", [])


tools = [
    {
        "type": "function",
        "name": "get_devices_by_client",
        "description": "Get the devices belonging to a client.",
        "parameters": {
            "type": "object",
            "properties": {
                "client_name": {
                    "type": "string",
                    "description": "The name of the client."
                }
            },
            "required": ["client_name"],
            "additionalProperties": False
        },
        "strict": True
    }
]


question = input("Tech > ")

response = ai.responses.create(
    model="gpt-6-luna",
    instructions="""
You are an IT support assistant.

Use the available tools when the user asks for client-specific information.
Do not invent client data.
Answer the technician naturally after receiving tool results.
""",
    tools=tools,
    input=question
)


for item in response.output:
    if item.type == "function_call":

        arguments = json.loads(item.arguments)

        if item.name == "get_devices_by_client":
            tool_result = get_devices_by_client(
                arguments["client_name"]
            )

            final_response = ai.responses.create(
                model="gpt-6-luna",
                tools=tools,
                previous_response_id=response.id,
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(tool_result)
                    }
                ]
            )

            print("\nNuvo Agent:")
            print(final_response.output_text)