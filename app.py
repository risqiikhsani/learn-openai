from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()

# generate text

# completion = client.chat.completions.create(
#     model="o1-mini",
#     store=True,
#     messages=[
#         {"role": "user", "content": "write a haiku about ai"}
#     ]
# )

# print(completion.choices[0].message.content)


# models that supports text and image input 

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    store=True,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
                    },
                },
            ],
        }
    ],
    max_tokens=300,
)

print(completion.choices[0].message.content)

