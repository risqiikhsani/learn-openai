import requests
import json
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()


def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']['temperature_2m']

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

messages = [{"role": "user", "content": "What's the weather like in Paris today?"}]

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# execute function code

# tool_call = completion.choices[0].message.tool_calls[0]
# args = json.loads(tool_call.function.arguments)

# result = get_weather(args["latitude"], args["longitude"])

# # supply models with result

# messages.append(completion.choices[0].message)  # append model's function call message
# messages.append({                               # append result message
#     "role": "tool",
#     "tool_call_id": tool_call.id,
#     "content": str(result)
# })

# When the model calls a function, you must execute it and return the result. Since model responses can include zero, one, or multiple calls, it is best practice to assume there are several.

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)
    # if name == "send_email":
    #     return send_email(**args)
    
messages.append(completion.choices[0].message)  # append model's function call message    
for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)

    result = call_function(name, args)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result)
    })

completion_2 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
)

# model response

print(completion_2.choices[0].message.content)