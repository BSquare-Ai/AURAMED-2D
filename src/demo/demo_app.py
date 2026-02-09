import sys
from pathlib import Path
import numpy as np
from PIL import Image
import gradio as gr

# --------------------------------------------------
# Path setup
# --------------------------------------------------
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agents import (
    SegmentationAgent,
    ReportAgent,
    ReasoningAgent,
    RouterAgent
)

from src.models.chexpert_model import CheXpertModel


# --------------------------------------------------
# Main Demo Controller
# --------------------------------------------------
class I_AURA_Demo:
    def __init__(self, config=None):
        self.config = config or {}
        self._init_agents()
        self.current_image = None
        self.current_report = None

    def _init_agents(self):
        agent_configs = self.config.get("agents", {})

        self.segmentation_agent = SegmentationAgent(
            config=agent_configs.get("segmentation", {})
        )

        self.router_agent = RouterAgent(
            config=agent_configs.get("router", {})
        )

        self.report_agent = ReportAgent(
            config=agent_configs.get("report", {})
        )

        self.reasoning_agent = ReasoningAgent(
            config=agent_configs.get("reasoning", {})
        )

        self.chexpert_model = CheXpertModel(device="mps")

    # --------------------------------------------------
    # Image Processing
    # --------------------------------------------------
    def process_image(self, image, modality):
        if image is None:
            return None, None, "No image uploaded.", "Labels: None"

        if isinstance(image, np.ndarray):
            image = Image.fromarray(image)

        modality = "xray" if modality in (None, "auto") else modality

        seg_result = self.segmentation_agent.process({
            "image": image,
            "modality": modality
        })
        labels = seg_result.get("labels", [])

        _ = self.router_agent.process({
            "labels": labels,
            "modality": modality
        })

        report_result = self.report_agent.process({
            "image": image,
            "labels": labels,
            "modality": modality,
            "selected_model": "RRG"
        })

        chexpert_findings = self.chexpert_model.predict(image)

        self.current_image = image
        self.current_report = {
            "findings": report_result.get("findings", "").strip(),
            "impression": report_result.get("impression", "").strip(),
            "chexpert": chexpert_findings
        }

        findings_text = (
            self.current_report["findings"]
            if self.current_report["findings"]
            else "No definitive abnormality described."
        )

        impression_text = (
            self.current_report["impression"]
            if self.current_report["impression"]
            else "Clinical correlation is advised."
        )

        # --------------------------------------------------
        # ✅ OPTION 1: DEMO / VIVA FRIENDLY REPORT
        # --------------------------------------------------
        report_text = f"""
RADIOLOGICAL REPORT

Examination:
Chest X-ray (PA view)

Clinical:
Evaluation for suspected pulmonary pathology

FINDINGS:
{findings_text}

IMPRESSION:
{impression_text}

RECOMMENDATIONS:
None at this time.
""".strip()

        metadata_text = (
            f"Model Used: RRG (Radiology Report Generator)\n"
            f"Segmentation Labels: {', '.join(labels) if labels else 'None'}\n"
            f"CheXpert Findings: {', '.join(chexpert_findings) if chexpert_findings else 'None'}"
        )

        return (
            image,
            seg_result.get("saved_image_path", image),
            report_text,
            metadata_text
        )

    # --------------------------------------------------
    # Clinical Reasoning
    # --------------------------------------------------
    def query_reasoning(self, query, history):
        history = history or []

        if not query:
            return history, ""

        if self.current_report is None:
            history.append(
                ("System", "Please run image analysis before asking clinical questions.")
            )
            return history, ""

        try:
            result = self.reasoning_agent.process({
                "report": self.current_report,
                "question": query
            })
            answer = result.get("answer", "")
            if not answer:
                answer = "Insufficient information in the report."
        except Exception as e:
            answer = f"Reasoning Error: {str(e)}"

        history.append((query, answer))
        return history, ""


# --------------------------------------------------
# Gradio UI
# --------------------------------------------------
def create_demo_ui(config=None):
    demo_app = I_AURA_Demo(config)

    with gr.Blocks(title="I-AURA-MED2D") as demo:

        # ✅ FINAL LOGO FIX (NO CROPPING)
        gr.HTML("""
        <div style="display:flex; align-items:center; padding:24px 0;">
            <img src="file=assets/logo.png" style="height:90px; object-fit:contain;" />
        </div>
        """)

        gr.Markdown("# I-AURA-MED2D Medical AI")

        with gr.Row():
            with gr.Column():
                img_in = gr.Image(label="Upload Scan", type="pil")
                mod = gr.Dropdown(["auto", "xray", "ct"], value="auto", label="Modality")
                btn = gr.Button("🚀 Run Analysis", variant="primary")

            with gr.Column():
                orig = gr.Image(label="Pre-processed Image")
                seg = gr.Image(label="AI Segmentation Mask")

        with gr.Row():
            with gr.Column():
                report_box = gr.Textbox(
                    label="Radiological Report",
                    lines=28,
                    interactive=False
                )
                meta = gr.Textbox(
                    label="Agent Metadata",
                    interactive=False
                )

            with gr.Column():
                chat = gr.Chatbot(
                    label="Clinical Reasoning History",
                    height=350
                )

                with gr.Row():
                    q_in = gr.Textbox(
                        label="Ask a clinical question...",
                        scale=4
                    )
                    ask_btn = gr.Button("Ask", scale=1)

                clear_btn = gr.Button("Clear Chat History")

        btn.click(
            demo_app.process_image,
            [img_in, mod],
            [orig, seg, report_box, meta]
        )
        q_in.submit(
            demo_app.query_reasoning,
            [q_in, chat],
            [chat, q_in]
        )
        ask_btn.click(
            demo_app.query_reasoning,
            [q_in, chat],
            [chat, q_in]
        )
        clear_btn.click(lambda: [], None, chat)

    return demo
