from enum import Enum
from typing import List
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

# generating a UI

class UIType(str, Enum):
    div = "div"
    button = "button"
    header = "header"
    section = "section"
    field = "field"
    form = "form"

class Attribute(BaseModel):
    name: str
    value: str

class UI(BaseModel):
    type: UIType
    label: str
    children: List["UI"] 
    attributes: List[Attribute]

UI.model_rebuild() # This is required to enable recursive types

class Response(BaseModel):
    ui: UI

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a UI generator AI. Convert the user input into a UI."},
        {"role": "user", "content": "Make a User Profile Form"}
    ],
    response_format=Response,
)

ui = completion.choices[0].message
print(completion.choices[0].message.content)
# If the model refuses to respond, you will get a refusal message
if (ui.refusal):
    print(ui.refusal)
else:
    print(ui.parsed)



