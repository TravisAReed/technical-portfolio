from ollama import chat
from pydantic import BaseModel
from typing import Literal


model = "medgemma1.5:4b"


class NumberChoice(BaseModel): #NumberChoice is our custom class name. we should be able to change that if we choose because i think it inherits from BaseModel
    choice: Literal["0", "1", "2"]


def choose_number(text: str) -> str:
    response = chat(
        model=model,
        messages=[
            {
                "role": "system", #system instructions
                "content": """
You are a strict number extractor.

Your task:
- Read the user's text.
- Choose exactly one value: "0", "1", or "2".
- Return JSON only.
- Do not explain.
- Do not include any text outside the JSON.

Meaning:
- Return {"choice": "0"} if the user is thinking of 0.
- Return {"choice": "1"} if the user is thinking of 1.
- Return {"choice": "2"} if the user is thinking of 2.
"""
            },
            {
                "role": "user",
                "content": text
            }
        ],
        format=NumberChoice.model_json_schema(), #make the model’s response match this JSON schema.
        options={
            "temperature": 0, #makes model max deterministic (good for classification but less creative)
            "num_predict": 20 #tells model to stop after generating up to about 20 tokens.
        }
    )

    result = NumberChoice.model_validate_json(response.message.content)
    return result.choice


print(choose_number("im thinking of the number 1"))