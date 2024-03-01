import torch
import langchain

if torch.cuda.is_available():
    torch.set_default_device('cuda')