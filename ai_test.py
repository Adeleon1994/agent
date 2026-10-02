from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-6-luna",
    input="Say hello to the Nuvo Agent project in one short sentence."
)

print(response.output_text)