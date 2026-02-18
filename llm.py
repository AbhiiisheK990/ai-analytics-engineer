from openai import OpenAI
client = OpenAI(api_key="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")

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
