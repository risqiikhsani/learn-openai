from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Supported types

# The following types are supported for Structured Outputs:

#     String
#     Number
#     Boolean
#     Integer
#     Object
#     Array
#     Enum
#     anyOf


client = OpenAI()

# getting a structured output 1

# from pydantic import BaseModel
# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]

# completion = client.beta.chat.completions.parse(
#     model="gpt-4o",
#    messages=[
#         {"role": "system", "content": "Extract the event information."},
#         {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
#     ],
#     response_format=CalendarEvent,
# )


# event = completion.choices[0].message.parsed
# print(event)
# print(completion.choices[0].message.content)

## getting a structured output 2

# class Step(BaseModel):
#     explanation: str
#     output: str

# class MathReasoning(BaseModel):
#     steps: list[Step]
#     final_answer: str

# completion = client.beta.chat.completions.parse(
#     model="gpt-4o-2024-08-06",
#     messages=[
#         {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
#         {"role": "user", "content": "how can I solve 8x + 7 = -23"}
#     ],
#     response_format=MathReasoning,
# )

# math_reasoning = completion.choices[0].message.parsed
# print(math_reasoning)
# print(completion.choices[0].message.content)

## getting a structured output 3

class User(BaseModel):
    name: str
    age: int
    email: str

class Users(BaseModel):
    users: list[User]

completion = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Get the users list."}],
    response_format=Users,
)

users = completion.choices[0].message
print(completion.choices[0].message.content)

# If the model refuses to respond, you will get a refusal message
if (users.refusal):
    print(users.refusal)
else:
    print(users.parsed)