import requests

API_URL = "https://router.huggingface.co/models/gpt2"
# Token is optional for public models; include it if you have rate limits or private models
headers = {"Authorization": "Bearer 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"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()
    except Exception:
        print("Non-JSON response:", response.status_code, response.text)
        return None

data = query({
    "inputs": "Write a short, factual sentence about radiology.",
    "parameters": {"max_new_tokens": 60}
})

print("Raw response:", data)

if isinstance(data, list) and "generated_text" in data[0]:
    print("Generated:", data[0]["generated_text"])
elif isinstance(data, dict) and "error" in data:
    print("Error from API:", data["error"])
else:
    print("Unexpected response format.")

