# I-AURA-MED2D Demo Application

Interactive web-based UI for testing the I-AURA-MED2D medical imaging pipeline.

## Features

- 📸 **Image Upload**: Upload medical images (X-ray, CT, MRI, etc.)
- 🎯 **Segmentation**: Automatic anatomical structure segmentation with visualization
- 📝 **Report Generation**: Generate radiology reports using RRG model
- 💬 **Interactive Q&A**: Query the reasoning agent with multiple questions
- 🔄 **Conversation History**: Maintain context across multiple queries

## Installation

### 1. Install Dependencies

```bash
cd /home/ajaid/I-AURA-MED2D
pip install -r requirements.txt
```

Key dependencies:
- `gradio>=4.0.0` - Web UI framework
- `matplotlib>=3.6.0` - Image visualization
- `torch>=2.0.0` - Deep learning
- `transformers>=4.30.0` - Model loading

### 2. Verify Model Setup

Ensure RRG model is downloaded:
```bash
ls models/rrg/default/
```

Should show: `config.json`, `model.safetensors`, tokenizer files, etc.

## Running the Demo

### Quick Start

```bash
cd /home/ajaid/I-AURA-MED2D
python scripts/run_demo.py
```

The demo will:
1. Load configuration from `configs/pipeline_config.yaml`
2. Initialize all agents (Segmentation, Router, Report, Reasoning)
3. Launch Gradio UI on `http://localhost:7860`

### Alternative: Direct Python

```python
from src.demo.demo_app import create_demo_ui
import yaml

# Load config
with open('configs/pipeline_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Create and launch
demo = create_demo_ui(config)
demo.launch(server_port=7860)
```

## Usage Guide

### Step 1: Upload Image
- Click on the image upload area
- Select a medical image (PNG, JPG, etc.)
- Or use sample images from IMIS dataset

### Step 2: Select Modality
- Choose imaging modality: X-ray, CT, MRI, Ultrasound, Endoscopy
- Or leave as "auto" for auto-detection

### Step 3: Process Image
- Click "Process Image" button
- Wait for:
  - Segmentation to complete
  - Report generation (RRG model)
  - Visualization of masked image

### Step 4: View Results
- **Original Image**: Your uploaded image
- **Segmented Image**: Image with overlay masks showing detected structures
- **Generated Report**: Radiology report from RRG model
- **Metadata**: Selected model and detected labels

### Step 5: Query Reasoning Agent
- Enter a question in the query box
- Or leave empty for default prompt: *"Generate an actual radiology report from this image, its mask and the ReportAgent report. Explain that report."*
- Click "Send Query" or press Enter
- View response in conversation history

### Step 6: Continue Conversation
- Ask follow-up questions
- The agent maintains conversation context
- Use "Clear Conversation" to reset

## Example Queries

1. **Default Prompt** (leave empty):
   ```
   Generate an actual radiology report from this image, its mask and the ReportAgent report. Explain that report.
   ```

2. **Specific Questions**:
   ```
   What abnormalities are visible in this chest X-ray?
   ```

3. **Follow-up Questions**:
   ```
   Can you explain the findings in more detail?
   What are the clinical implications?
   ```

4. **Report Refinement**:
   ```
   Generate a more detailed radiology report
   ```

## Workflow

```
Medical Image
    ↓
[SegmentationAgent] → Masks + Labels
    ↓
[RouterAgent] → Select RRG Model
    ↓
[ReportAgent] → Generate Report (RRG)
    ↓
[ReasoningAgent] ← User Queries
    ↓
Enhanced Explanations & Q&A
```

## Configuration

Edit `configs/pipeline_config.yaml` to:
- Set model paths
- Configure device (CPU/GPU)
- Adjust agent parameters

## Troubleshooting

### Issue: "Model not found"
**Solution**: Ensure RRG model is downloaded:
```bash
python scripts/download_rrg_simple.py
```

### Issue: "CUDA out of memory"
**Solution**: Set device to CPU in config:
```yaml
agents:
  report:
    device: "cpu"
```

### Issue: "Gradio not found"
**Solution**: Install Gradio:
```bash
pip install gradio>=4.0.0
```

### Issue: "IMIS-Bench not found"
**Solution**: Ensure IMIS-Bench is in parent directory or update paths in config.

## Sample Images

To use sample images from IMIS dataset:

```python
from scripts.load_imis_sample import find_imis_images, load_sample_image

# Find images
images = find_imis_images()
if images:
    image = load_sample_image(images[0])
    # Use in demo
```

Or manually place images in:
- `IMIS-Bench/dataset/`
- `IMIS-Bench/demo_image/`

## Architecture

The demo application (`src/demo/demo_app.py`) includes:

- **I_AURA_Demo**: Main demo class
  - `process_image()`: Full pipeline processing
  - `query_reasoning()`: Interactive Q&A
  - `_create_masked_image()`: Visualization
  - `_format_report_text()`: Report formatting

- **Gradio UI**: Web interface
  - Image upload/display
  - Report visualization
  - Chat interface for queries
  - Conversation history

## Next Steps

1. **Add BiomedGPT Checkpoints**: For enhanced reasoning
2. **Add More Models**: S4M, additional RRG variants
3. **Export Reports**: Save generated reports
4. **Batch Processing**: Process multiple images
5. **Advanced Visualization**: 3D masks, interactive overlays

## Notes

- The demo uses placeholder reasoning if BiomedGPT checkpoints are not available
- Segmentation uses IMIS-Bench (ensure it's configured)
- Reports are generated using RRG model (downloaded)
- Conversation history is maintained per session

## Support

For issues or questions:
1. Check `MODEL_INSTALLATION_STATUS.md`
2. Review `IMPLEMENTATION_STATUS.md`
3. Check agent logs in the terminal

