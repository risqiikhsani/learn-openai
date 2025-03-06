from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# You can define structured fields to extract from unstructured input data, such as research papers.


client = OpenAI()
class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
        {"role": "user", "content": "..."}
    ],
    response_format=ResearchPaperExtraction,
)

research_paper = completion.choices[0].message

print(completion.choices[0].message.content)

# If the model refuses to respond, you will get a refusal message
if (research_paper.refusal):
    print(research_paper.refusal)
else:
    print(research_paper.parsed)