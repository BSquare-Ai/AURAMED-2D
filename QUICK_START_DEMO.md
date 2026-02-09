# Quick Start: I-AURA-MED2D Demo

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd /home/ajaid/I-AURA-MED2D
pip install gradio>=4.0.0 matplotlib>=3.6.0
pip install torch torchvision transformers
```

### 2. Run Demo

```bash
python scripts/run_demo.py
```

### 3. Open Browser

Navigate to: `http://localhost:7860`

## 📋 What the Demo Does

1. **Upload Image** → Medical image (X-ray, CT, etc.)
2. **Process** → Runs:
   - Segmentation (IMIS-Bench)
   - Routing (selects RRG)
   - Report Generation (RRG model)
3. **Visualize** → Shows:
   - Original image
   - Masked/segmented image
   - Generated report
4. **Query** → Ask questions:
   - Default: "Generate an actual radiology report from this image, its mask and the ReportAgent report. Explain that report."
   - Or custom questions
5. **Continue** → Multiple queries with conversation history

## 🎯 Key Features

✅ **Image Processing**: Upload any medical image
✅ **Segmentation**: Automatic anatomical structure detection
✅ **Report Generation**: RRG model generates radiology reports
✅ **Mask Visualization**: Color-coded overlay of detected structures
✅ **Interactive Q&A**: Query reasoning agent with multiple questions
✅ **Conversation History**: Maintains context across queries

## 📝 Example Workflow

```
1. Upload chest X-ray image
2. Click "Process Image"
   → Segmentation runs
   → RRG generates report
   → Masked image displayed
3. Query box (leave empty for default):
   → "Generate an actual radiology report..."
4. View response in conversation
5. Ask follow-up: "Explain the findings"
6. Continue conversation...
```

## 🔧 Configuration

Models are configured in `configs/pipeline_config.yaml`:

- **RRG Model**: `models/rrg/default` (already downloaded ✅)
- **BiomedGPT**: Configure when checkpoints available
- **Device**: Auto-detects GPU/CPU

## ⚠️ Requirements

- Python 3.8+
- PyTorch (for models)
- Gradio (for UI)
- RRG model downloaded (✅ done)
- IMIS-Bench in parent directory (for segmentation)

## 🐛 Troubleshooting

**"Module not found"**: Install dependencies
```bash
pip install -r requirements.txt
```

**"Model not found"**: Download RRG
```bash
python scripts/download_rrg_simple.py
```

**"CUDA error"**: Use CPU
```yaml
# In configs/pipeline_config.yaml
agents:
  report:
    device: "cpu"
```

## 📚 More Info

- Full documentation: `DEMO_README.md`
- Model status: `MODEL_INSTALLATION_STATUS.md`
- Implementation: `IMPLEMENTATION_STATUS.md`

