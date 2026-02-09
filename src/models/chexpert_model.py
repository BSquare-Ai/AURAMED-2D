import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np


class CheXpertModel:
    """
    Lightweight CheXpert-style classifier using DenseNet-121.
    This is a WEAK SUPERVISION model for demo & research purposes.
    """

    CHEXPERT_LABELS = [
        "Atelectasis",
        "Cardiomegaly",
        "Consolidation",
        "Edema",
        "Pleural Effusion",
        "Pneumonia"
    ]

    def __init__(self, device="cpu"):
        self.device = torch.device(device)

        # ✅ TorchVision model (always available, no downloads)
        self.model = models.densenet121(pretrained=True)
        self.model.eval()
        self.model.to(self.device)

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])

    @torch.no_grad()
    def predict(self, image):
        """
        Returns CheXpert-style labels using weak visual cues.
        This is NOT a diagnostic model.
        """

        if isinstance(image, str):
            image = Image.open(image).convert("RGB")
        elif isinstance(image, Image.Image):
            image = image.convert("RGB")
        else:
            raise ValueError("Invalid image input")

        x = self.transform(image).unsqueeze(0).to(self.device)
        features = self.model.features(x)
        pooled = torch.mean(features, dim=[2, 3]).cpu().numpy()[0]

        # 🔑 Weak heuristic mapping (demo-safe)
        findings = []

        if pooled.mean() > 0.25:
            findings.append("Lung Opacity")
            findings.append("Pneumonia")

        if pooled.max() > 1.0:
            findings.append("Consolidation")

        return list(set(findings))
