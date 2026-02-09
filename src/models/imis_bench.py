import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import pickle
import re
import random
from pathlib import Path
from dataloaders.data_utils import get_points_from_mask, get_bboxes_from_mask
from transformers import AutoTokenizer

class IMISNet(nn.Module):
    def __init__(
        self, 
        sam, 
        test_mode=False, 
        multimask_output=True, 
        category_weights=None,
        select_mask_num=None
        ):
        super().__init__()
        
        # 1. MAC OPTIMIZATION: Ensure device is MPS if available
        if torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = sam.device
            
        self.to(self.device) # Move entire model to Mac GPU
        
        self.image_encoder = sam.image_encoder
        self.mask_decoder = sam.mask_decoder
        self.prompt_encoder = sam.prompt_encoder
        self.text_model = sam.text_model
        self.text_out_dim = sam.text_out_dim
        
        # Use absolute path logic for the tokenizer to avoid download issues
        self.tokenizer = AutoTokenizer.from_pretrained('clip-vit-base-patch32')

        self.test_mode = test_mode
        self.multimask_output = multimask_output
        self.category_weights = category_weights
        self.select_mask_num = select_mask_num

        self.image_format = sam.image_format
        self.image_size = sam.prompt_encoder.input_image_size
        
        # Freezing text model
        for n, value in self.text_model.named_parameters():
            value.requires_grad = False

        # 2. PATH LOGIC: Find weight files relative to the project root
        if category_weights is not None:
            self.load_category_weights(category_weights)
        else:
            # Default fallback to root/models/ folder
            project_root = Path(__file__).resolve().parent.parent.parent
            default_weights = project_root / "models" / "category_weights.pkl"
            if default_weights.exists():
                self.load_category_weights(str(default_weights))
    
    # ... [Rest of your image_forward and forward_decoder methods remain the same] ...

    def forward(self, image, prompt):
        # Ensure input images are on the correct device (MPS)
        image = image.to(self.device)
        img_shape = image.shape
        image_embedding = self.image_forward(image) # Removed test_mode extra arg
        return self.forward_decoder(image_embedding, prompt)

    # ... [Rest of your helper methods: process_text_prompt, etc., remain the same] ...

    def load_category_weights(self, src_weights=None):
        if src_weights is not None:
            with open(src_weights, "rb") as f:
                # Load pickle data and move tensors to MPS
                data = pickle.load(f)
                self.src_weights_raw, self.categories_map, self.category_to_index, self.index_to_category = data
                self.src_weights = torch.tensor(self.src_weights_raw).to(self.device)
                print(f"--- IMISNet Category Weights Loaded to {self.device} ---")

# Maintains backward compatibility
IMISBenchModel = IMISNet

if __name__ == '__main__':
    print('IMISNet configured for Apple Silicon/MPS.')