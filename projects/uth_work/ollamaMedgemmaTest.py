from ollama import chat

response = chat(
    model="medgemma1.5:4b", #had to first run "ollama pull medgemma1.5:4b" then checked with "ollama list"
    messages=[
        {
            "role": "user",
            "content": "Explain in simple terms what high fasting glucose can indicate."
        }
    ],
)

print(response.message.content)


print("\n--- timing ---")
print("total seconds:", response.total_duration / 1e9)
print("load seconds:", response.load_duration / 1e9)
print("prompt processing seconds:", response.prompt_eval_duration / 1e9)
print("generation seconds:", response.eval_duration / 1e9)
print("input tokens:", response.prompt_eval_count)
print("output tokens:", response.eval_count)