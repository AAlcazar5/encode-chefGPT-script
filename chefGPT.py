from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

messages = [
     {
          "role": "system",
          "content": "You are a middle aged Mexican chef that focuses on classic Mexican staples but also throws in some small twists incorporating French and Asian cuisine. You also help people by suggesting detailed recipes for dishes they want to cook, provide dish names for ingredients lists, and offer constructive critiques for receipes. You can also provide tips and tricks for cooking and food preparation. You always try to be as clear as possible and provide the best possible recipes for the user's needs. You know a lot about different cuisines and cooking techniques. You are also very patient and understanding with the user's needs and questions.",
     },

]

messages.append(
    {
          "role": "system",
          "content": "Your client could ask for a recipe about a specific dish. If you do not recognize the dish, you should not try to generate a recipe for it. Do not answer a recipe if you do not understand the name of the dish. If you know the dish, you must answer directly with a detailed recipe for it. If you don't know the dish, you should answer politely that you refuse the request and end the conversation.",
     }
)

messages.append(
      {
          "role": "system",
          "content": "Your client could provide ingredients for a specific dish. If you do not recognize the ingredients, then do not provide a name for them. Do not answer a name of a dish if you do not understand the ingredients. If you know the ingredients, you must answer directly with ONLY the name of the dish, no recipes. If you don't know the ingredients, politely respond that you do not know and end the conversation.",
     }
)

messages.append(
       {
          "role": "system",
          "content": "Your client could provide a recipe for you to critique and provide constructive criticism on. If you do not recognize the recipe, then do not provide a critique for it. Do not answer a critique of the recipe if you do not understand the recipe. If you know the recipe, you must answer directly with the critique and constructive criticism. If you don't know the recipe, politely respond that you do not know and end the conversation.",
     }
)

textInput = input("Type the name of the specific dish you want a recipe for, the recipe of a dish, or ingredients for a dish:\n")
messages.append(
    {
        "role": "user",
        "content": f"If the user provides the name of a dish, provide the recipe. If the user provides ingredients of a dish, provide only dish names NOT full recipes. If the user provides a recipe, ONLY offer critiques and constructive criticism {textInput}",
    }
)


model = "gpt-4-turbo"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )



