import numpy as np
import torch

def get_points_from_mask(mask, get_point=1):
    if isinstance(mask, torch.Tensor):
        mask = mask.cpu().numpy()

    coords = np.argwhere(mask == 1)

    if coords.shape[0] == 0:
        H, W = mask.shape
        coords = np.random.randint(0, H, size=(10, 2))

    selected = coords[np.random.choice(coords.shape[0], get_point, replace=True)]
    labels = np.ones((get_point,), dtype=np.int64)

    return selected[:, [1, 0]], labels

def get_bboxes_from_mask(mask):
    if isinstance(mask, torch.Tensor):
        mask = mask.cpu().numpy()

    ys, xs = np.where(mask == 1)

    if len(xs) == 0:
        return torch.tensor([0, 0, 0, 0])

    x1, y1 = xs.min(), ys.min()
    x2, y2 = xs.max(), ys.max()

    return torch.tensor([x1, y1, x2, y2], dtype=torch.float32)
