from ollama import chat
from pydantic import BaseModel
from typing import Literal

#choose your model here
# model = "medgemma1.5:4b"
model = "medgemma:27b"

#these are the instructions the model will take in every time on how to classify
instr = ""


class BucketChoice(BaseModel):
    #replace the options in the list with whatever options you want the model to choose from
    choice: Literal["less than -1", "-1", "0", "1", "more than 1"] 
    


def classify_response(question: str, user_answer: str) -> str:
    #resets timer of how model staying active everytime chat() is called
    response = chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"{instr}"
            },
            {
                "role": "user",
                "content": f"""
Question:
{question}

Patient response:
{user_answer}
"""
            }
        ],
        format=BucketChoice.model_json_schema(),
        options={
            "temperature": 0, #temperature of 0 maximizes deterministic trait of model
            "num_predict": 20 #limits number of tokens model can respond with
        }
    )

    result = BucketChoice.model_validate_json(response.message.content)
    return result.choice

















# print(classify_response("Choose a number 0-2:", "im thinking of the number 1"))
# print(classify_response("Choose a number 0 through 2:", "im thinking of the number 1"))
# print(classify_response("Choose a number 0 to 2:", "im thinking of the number 1"))


# print(classify_response("Choose a number 0-2:", "i ate an alligator and am confused"))

