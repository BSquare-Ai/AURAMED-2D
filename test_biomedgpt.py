from src.models.biomedgpt_model import BiomedGPTModel

rrg_report = """
FINDINGS:
Patchy opacities are seen in the right lower lung zone.
No pleural effusion is noted.

IMPRESSION:
Features are suggestive of mild pneumonia.
"""

model = BiomedGPTModel()

answer = model.answer_question(
    question="""What abnormality is seen in the lungs?
A. No abnormality is seen.
B. Patchy opacities are seen in the right lower lung zone.""",
    context=rrg_report
)

print(answer)
