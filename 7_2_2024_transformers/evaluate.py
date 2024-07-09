import matplotlib.pyplot as plt
import torch
from data import PAD_TOKEN, padding_mask, parenthesization_to_tensor


class ConfusionMatrix:
    def __init__(self, confusion_matrix):
        self.confusion_matrix = confusion_matrix

    def __str__(self):
        return str(self.confusion_matrix)

    def print_accuracy(self):
        """
        Prints out the accuracy within each of the prediction classes and the overall accuracy.
        """
        confusion_matrix = self.confusion_matrix
        num_classes = len(confusion_matrix)
        for i in range(num_classes):
            print(
                f"Accuracy for class {i} = {100 * confusion_matrix[i][i] / sum(confusion_matrix[i])}%"
            )

        total_correct = sum([confusion_matrix[i][i] for i in range(num_classes)])
        total = sum([sum(confusion_matrix[i]) for i in range(num_classes)])
        print(f"Overall accuracy = {100 * total_correct / total}%")

    def plot(self, title="Confusion Matrix"):
        """
        Plots the confusion matrix as a heatmap.
        """
        confusion_matrix = self.confusion_matrix
        plt.imshow(confusion_matrix, cmap="Blues")
        plt.xticks(range(len(confusion_matrix)), range(len(confusion_matrix)))
        plt.yticks(range(len(confusion_matrix)), range(len(confusion_matrix)))
        plt.xlabel("Predicted label")
        plt.ylabel("True label")
        for i in range(len(confusion_matrix)):
            for j in range(len(confusion_matrix)):
                plt.text(j, i, confusion_matrix[i][j], ha="center", va="center")
        plt.title(title)
        plt.show()


def evaluate_model(model, dataloader):
    """
    Evaluates the model using the provided dataloader and returns the confusion matrix.

    Args:
        model (torch.nn.Module): The model to be evaluated.
        dataloader (torch.utils.data.DataLoader): The dataloader used for evaluation.

    Returns:
        ConfusionMatrix: A 2x2 confusion matrix where rows represent true labels and columns represent predicted labels.
    """

    model.eval()

    with torch.no_grad():
        confusion_matrix = [[0, 0], [0, 0]]
        for data in dataloader:
            inputs, labels = data
            output = model(inputs, mask=padding_mask(inputs))
            predictions = torch.argmax(torch.select(output, 1, 0), dim=1)
            for label, prediction in zip(labels, predictions):
                confusion_matrix[label][prediction] += 1
        return ConfusionMatrix(confusion_matrix)


def predict(model, single_input):
    """
    Predicts the output based on the provided model and single input.

    Args:
        model: The model used for prediction.
        single_input: The input data for prediction.

    Returns:
        The predicted output based on the model and input.
    """
    t = parenthesization_to_tensor(single_input)
    output = model(t, mask=padding_mask(t))

    #awawawa = torch.select(output, 0, 0)
    #awawawawawa = torch.argmax(torch.select(output, 0, 0))
    #print(f"PREDCTION: {output} )-( {awawawa} )-( {awawawawawa}")

    return torch.argmax(torch.select(output, 0, 0))
