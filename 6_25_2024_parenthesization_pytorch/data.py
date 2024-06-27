import csv
import torch
from torch.utils.data import Dataset, DataLoader, random_split
import torch.nn.functional as F
from torch import nn

device = "cpu"

def parenthesization_to_tensor(parenthesization):
    """
    Convert a parenthesization string to a pytorch tensor representation.

    Args:
        parenthesization (str): The parenthesization string to convert.

    Returns:
        torch.Tensor: The tensor representation of the parenthesization.
        The tensor has shape (4*n), where 2*n is the length of the parenthesization string.
        Each element in the tensor is either 0 or 1, representing whether the corresponding
        parenthesization character is "(" or ")".
    """
    tens = torch.tensor([])
    for char in parenthesization:
        if char == "(":
            tens = torch.cat((tens, torch.tensor([1, 0])))
        elif char == ")":
            tens = torch.cat((tens, torch.tensor([0, 1])))
        else: 
            raise ValueError("Invalid character in parenthesization string")
    return tens

class ParenthesizationDataset(Dataset):
    def __init__(self, n):
        self.data = []
        filename = f"data/parenthesizations_{n}.csv"
        with open(filename, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                self.data.append((parenthesization_to_tensor(row["parenthesization"]), int(row["valid"])))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

class ParenthesizationModel(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.fc = nn.Linear(2*2*n, 2)

    def forward(self, x):
        return self.fc(x)