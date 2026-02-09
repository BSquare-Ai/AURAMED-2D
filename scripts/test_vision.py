import base64
from huggingface_hub import InferenceClient

# Initialize Cloud Client
client = InferenceClient(api_key="your_token_here")

def analyze_medical_image_cloud(image_path, question):
    """
    Since we are using the cloud, we send the findings as text.
    In a full pipeline, your 'segmentation' agent provides these findings.
    """
    
    # 1. SIMULATED FINDINGS (In your real app, your segmentation model provides this)
    # For this test, let's assume the segmenter found these:
    findings = "Segmented area: Lower left lung lobe shows increased opacity. No pleural effusion."
    
    # 2. PROMPT FOR BIOMEDGPT
    prompt = f"""[INST] <<SYS>>
You are a medical reasoning AI. Use the image findings to answer the question.
<</SYS>>
Findings: {findings}
Question: {question} [/INST]"""

    print("--- Sending Reasoning Task to BioMedGPT Cloud ---")
    
    try:
        response = client.text_generation(
            model="PharMolix/BioMedGPT-LM-7B",
            prompt=prompt,
            max_new_tokens=300
        )
        return response
    except Exception as e:
        return f"Error: {e}"

# Run the test
output = analyze_medical_image_cloud("test_xray.jpg", "What is the likely diagnosis based on these findings?")
print("\nMODEL OUTPUT:")
print(output)