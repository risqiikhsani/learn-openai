import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()


def send_email(to_address, subject, body):
    # Simulated email sending function
    print(f"Sending email to {to_address}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    return "Email sent successfully"

tools = [{
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to a specified address",
        "parameters": {
            "type": "object",
            "properties": {
                "to_address": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to_address", "subject", "body"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

messages = [{"role": "user", "content": "Please send an email to john@example.com about the project update"}]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
)

messages.append(completion.choices[0].message)
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    if name == "send_email":
        result = send_email(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

final_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools,
)

print(final_response.choices[0].message.content)

