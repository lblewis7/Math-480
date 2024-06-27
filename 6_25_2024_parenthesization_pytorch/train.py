import torch
def train_one_epoch(training_loader, model, loss_fn, optimizer):
    """
    Trains the model for one epoch using the given training data loader, model, loss function, and optimizer.
    
    Args:
        training_loader (torch.utils.data.DataLoader): The data loader for the training data.
        model (torch.nn.Module): The model to be trained.
        loss_fn (torch.nn.loss._Loss): The loss function used to compute the loss.
        optimizer (torch.optim.Optimizer): The optimizer used to update the model parameters.
        
    Returns:
        float: The total loss computed over the entire epoch.
    """
    # TODO: Use https://pytorch.org/tutorials/beginner/introyt/trainingyt.html#the-training-loop as a reference.
    model.train()  # Set the model to training mode
    total_loss = 0.0
    
    for batch_idx, (inputs, targets) in enumerate(training_loader):
        optimizer.zero_grad()  # Zero the gradients
        outputs = model(inputs)  # Forward pass
        loss = loss_fn(outputs, targets)  # Compute the loss
        loss.backward()  # Backpropagation
        optimizer.step()  # Update model parameters
        
        total_loss += loss.item()
    
    return total_loss / len(training_loader)  # Average loss per batch

def evaluate_model(model, test_dataset):
    """
    Evaluates the model using the provided test dataset and returns the confusion matrix.

    Args:
        model (torch.nn.Module): The model to be evaluated.
        test_dataset (torch.utils.data.Dataset): The dataset used for evaluation.

    Returns:
        list: A 2x2 confusion matrix where rows represent true labels and columns represent predicted labels.
    """
    model.eval() # Set the model to evaluation mode

    with torch.no_grad():
        confusion_matrix = [[0, 0], [0, 0]]
        for inputs, targets in test_dataset:
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            for i in range(targets.size(0)):
                confusion_matrix[targets[i]][predicted[i]] += 1

    return confusion_matrix
