import requests
import time

# Use the 7B model for better medical reasoning
API_URL = "https://api-inference.huggingface.co/models/PharMolix/BioMedGPT-LM-7B"
headers = {"Authorization": "Bearer YOUR_NEW_TOKEN_HERE"}

def query_biomed(payload):
    while True:
        response = requests.post(API_URL, headers=headers, json=payload)
        data = response.json()
        
        # Check if the model is still loading on Hugging Face's servers
        if isinstance(data, dict) and "estimated_time" in data:
            wait_time = data['estimated_time']
            print(f"Model is waking up... waiting {round(wait_time)} seconds.")
            time.sleep(wait_time)
            continue
            
        return data

# Test input
test_data = {
    "inputs": "[INST] What are the key findings in this chest X-ray? [/INST]",
    "parameters": {"max_new_tokens": 150, "temperature": 0.2}
}

print("Consulting BioMedGPT...")
result = query_biomed(test_data)

if result and isinstance(result, list):
    print("\n--- Response ---\n", result[0]["generated_text"])
else:
    print("Error:", result)