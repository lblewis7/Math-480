import matplotlib.pyplot as plt
import torch

from data import PAD_TOKEN, padding_mask


def plot_linear_layer(
    layer,
):
    """
    Plots a heatmap of the weights for a linear layer.

    Parameters:
        layer (nn.Linear): The Linear layer for which the weights are to be visualized.
    """
    # Get the weights from the layer
    weights = layer.weight.data

    # Normalize the weights (optional)
    weights_normalized = torch.abs(weights) / torch.max(torch.abs(weights))

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    plt.imshow(weights_normalized, cmap='coolwarm', aspect='auto')
    plt.colorbar(label='Normalized Weight Magnitude')
    plt.title(f"Heatmap of Weights for Layer {layer.__class__.__name__}")
    plt.xlabel("Output Units")
    plt.ylabel("Input Units")
    plt.show()


def incorrect_predictions(model, dataloader):
    """
    Given a model and a dataloader, this function evaluates the model by predicting the labels for each input in the dataloader.
    It keeps track of incorrect predictions and returns a list of inputs that were incorrectly predicted for each label.

    Args:
        model (torch.nn.Module): The model used for prediction.
        dataloader (torch.utils.data.DataLoader): The dataloader containing the input data.

    Returns:
        List[List[List[int]]]: A list of incorrect predictions for each label. The list contains two sublists, one for each label.
            Each sublist contains a list of inputs that were incorrectly predicted for that label.
            Each input is represented as a list of integers.
    """
    model.eval()

    with torch.no_grad():
        incorrect_predictions = [[], []]

        """
        for inputs, targets in dataloader: 
            outputs = model(inputs)
            print(inputs, outputs)
            _, predicted = torch.max(outputs.data, 1)
            print(predicted, targets)
            for i in range(targets.size(0)):
                print(predicted[i], targets[i])
                if predicted[i] != targets[i]:
                    incorrect_predictions[targets[i]].append(inputs[i])
        """

        for data in dataloader:
            inputs, labels = data
            output = model(inputs, mask=padding_mask(inputs))
            predictions = torch.argmax(torch.select(output, 1, 0), dim=1)
            for label, prediction in zip(labels, predictions):
                if label != prediction:
                    incorrect_predictions[label].append(inputs[label])

        return incorrect_predictions


def token_contributions(model, single_input):
    """
    Calculates the contributions of each token in the single_input sequence to each class in the model's
    predicted output. The contribution of a single token is calculated as the difference between the
    model output with the given input and the model output with the single token changed to the other
    parenthesis.

    Args:
        model (torch.nn.Module): The model used for prediction.
        single_input (torch.Tensor): The input sequence for which token contributions are calculated.

    Returns:
        List[float]: A list of contributions of each token to the model's output.
    """
    output = model(single_input, mask=padding_mask(single_input))
    output = torch.select(output, 0, 0)
    #print()
    #print()
    #print(">>>> NEW INPUT ", single_input, " <<<<")
    #print("output", output)

    result = []

    for i in range(1, 23): # this range could be entirely wrong (EDIT: LIKELY CORRECT)
        if single_input[i] == 3: break
        new_input = single_input.clone()
        #print()
        new_input[i] = 1 - single_input[i] # could also be entirely wrong
        #print(f"AFTER {i} - new input ", new_input)
        new_output = model(new_input, mask=padding_mask(new_input))
        new_output = torch.select(new_output, 0, 0)
        #print("new output", new_output)
        result.append((new_output[1] - new_output[0]) - (output[1] - output[0])) # idk something like this maybe
        #print(">> APPENDED ", result.pop())

    #print("result", result)
    return result

def activations(model, dataloader):
    """
    Returns the frequency of each hidden feature's activation in the feedforward layer of the model
    over all inputs in the dataloader.

    Args:
        model (torch.nn.Module): The model used for prediction.
        dataloader (torch.utils.data.DataLoader): The dataloader containing the input data.

    Returns:
        List[int]: A list of frequencies for each hidden feature in the feedforward layer of the model.
    """
    result = []
    

    # Initialize a dictionary to store activation counts
    activation_counts = {}

    # Set the model to evaluation mode
    model.eval()

    with torch.no_grad():
        for inputs, _ in dataloader:
            # Forward pass to get activations
            activations = model(inputs)

            # Count activations for each feature
            for activation in activations:
                for feature in activation:
                    feature_key = tuple(feature.tolist())
                    #print("COOL AREA 1")
                    #print(feature_key)
                    #print(feature.type())
                    activation_counts.get(feature_key, 0)
                    activation_counts[feature_key] = activation_counts.get(feature_key, 0) + 1

    # Convert the dictionary to a list of frequencies
    for key, value in activation_counts.items():
        #for _ in range(value):
        result.append(value) #key

    return result
