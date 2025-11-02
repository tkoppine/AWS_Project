import torch
import os

data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'data.pt')
names = torch.load(data_path)[1]
print(names)