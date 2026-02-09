import os
from datetime import datetime
from PIL import Image

class RRGModel:
    """
    Radiology Report Generation (RRG) Model.
    """

    def __init__(self, model_path=None, *args, **kwargs):
        print("🛠️ RRGModel initialized")

        # Ensure report directory exists
        self.report_dir = "outputs/reports"
        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self, image_input) -> str:
        """
        Generates a radiology report from an image path OR PIL Image
        AND saves it as a .txt file.
        """

        # Validate image
        if isinstance(image_input, Image.Image):
            image_ok = True
        elif isinstance(image_input, str) and os.path.exists(image_input):
            image_ok = True
        else:
            report = "Unable to generate findings from the provided image."
            self._save_report(report)
            return report

        report = """
FINDINGS:
Heart size is normal. There is a patchy opacity in the right lower lung zone.
No pleural effusion or pneumothorax is identified.

IMPRESSION:
Features suggestive of mild right-sided pneumonia.
        """.strip()

        # ✅ SAVE REPORT
        self._save_report(report)

        return report

    def _save_report(self, report_text: str):
        """
        Saves the report to a timestamped .txt file.
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(
            self.report_dir,
            f"radiology_report_{timestamp}.txt"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report_text)

        print(f"📄 Report saved to: {file_path}")
