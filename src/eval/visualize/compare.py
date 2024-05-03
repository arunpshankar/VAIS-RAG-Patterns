from src.config.logging import logger
import matplotlib.pyplot as plt
from typing import List
import os


def plot_answer_quality(data: List[List[float]], labels: List[str], categories: List[str]):
    """
    Generates a bar chart for comparing response classes across different approaches for question answering.
    Saves the plot to a specified directory.
    
    Parameters:
        data (List[List[float]]): A list of lists, where each sublist contains percentages
                                   for 'Correct', 'Partially Correct', and 'Incorrect' classes.
        labels (List[str]): Labels for each approach to appear in the legend.
        categories (List[str]): Names of the response classes ('Correct', 'Partially Correct', 'Incorrect').
    
    Returns:
        None
    """
    try:
        _, ax = plt.subplots(figsize=(10, 7))
        bar_width = 0.2
        index = range(len(categories))

        # Create bars for each approach
        for i, approach in enumerate(data):
            ax.bar([p + i * bar_width for p in index], approach, bar_width, label=labels[i])

        ax.set_xlabel('Class')
        ax.set_ylabel('%')
        ax.set_title('Answer Quality by Approach')
        ax.set_xticks([p + 1.5 * bar_width for p in index])
        ax.set_xticklabels(categories, fontsize=9)
        ax.legend()

        # Ensure the directory exists
        directory = './data/plots'
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Directory {directory} created.")

        # Save the plot
        plot_path = os.path.join(directory, 'answer_quality_by_approach.png')
        plt.savefig(plot_path)
        logger.info(f"Plot saved to {plot_path}.")

    except Exception as e:
        logger.error(f"Failed to generate and save plot: {e}")


if __name__ == "__main__":
    # Example data and labels
    categories = ['Correct', 'Partially Correct', 'Incorrect']
    data = [
        [14.00, 64.00, 22.00],  # OOB
        [14.14, 71.72, 14.14],  # OOB+Filters
        [38.00, 54.00, 8.00],   # Extractive Segments
        [40.40, 52.53, 7.07]    # Extractive Answers
    ]
    labels = ['OOB', 'OOB+Filters', 'Extractive Segments', 'Extractive Answers']

    plot_answer_quality(data, labels, categories)
