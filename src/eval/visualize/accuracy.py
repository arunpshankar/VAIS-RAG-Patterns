from src.config.logging import logger 
import matplotlib.pyplot as plt
from typing import List
import os


def plot_accuracy_chart(data: List[float], categories: List[str], colors: List[str], title: str, xlabel: str, ylabel: str, save_path: str) -> None:
    """
    Generates and displays a bar chart with the specified attributes and saves it to a specified path.

    Args:
    data (List[float]): A list of accuracies for each category.
    categories (List[str]): A list of names for each category.
    colors (List[str]): A list of colors for each bar in the chart.
    title (str): The title of the chart.
    xlabel (str): The label for the x-axis.
    ylabel (str): The label for the y-axis.
    save_path (str): The path where the chart will be saved.

    Raises:
    ValueError: If the length of data, categories, and colors are not the same.
    """

    if len(data) != len(categories) or len(categories) != len(colors):
        logger.error("Input lists must have the same length.")
        raise ValueError("Data, categories, and colors lists must have the same length.")

    try:
        # Create figure
        plt.figure(figsize=(8, 5))
        _ = plt.bar(categories, data, color=colors, width=0.6, hatch='...')

        # Set titles and labels with updated font sizes
        plt.title(title, fontsize=12)
        plt.xlabel(xlabel, fontsize=10)
        plt.ylabel(ylabel, fontsize=10)
        plt.xticks(fontsize=8)
        plt.yticks(fontsize=8)

        # Set y-axis limits and grid
        plt.ylim(0, 1)
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Display the plot with a tight layout
        plt.tight_layout()
        # plt.show()

        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Save the figure
        plt.savefig(save_path)
        logger.info(f"Chart saved successfully at {save_path}")

    except Exception as e:
        logger.error(f"Failed to generate or save chart: {e}")
        raise

# Data setup
accuracy_data = [0.46, 0.52, 0.65, 0.67]
labels = ['OOB', 'OOB+Filters', 'Extractive Segments', 'Extractive Answers']
colors = ['#add8e6', '#90ee90', '#ffb6c1', '#dda0dd']  # Light blue, light green, light pink, light purple

# Call the function with the necessary parameters and path to save the plot
plot_accuracy_chart(accuracy_data, labels, colors, 'Answer Accuracy by Approach', 'Approach', 'Accuracy', './data/plots/accuracy.png')
