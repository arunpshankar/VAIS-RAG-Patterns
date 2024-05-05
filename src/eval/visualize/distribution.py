from src.config.logging import logger
import matplotlib.pyplot as plt
import pandas as pd
import os


# Default plot configurations
DEFAULT_PLOT_WIDTH = 10  # Adjust as needed
DEFAULT_PLOT_HEIGHT = 8  # Adjust as needed

def create_semantic_similarity_boxplot(data: pd.DataFrame, save_dir: str, 
                                      plot_width: int = DEFAULT_PLOT_WIDTH, plot_height: int = DEFAULT_PLOT_HEIGHT) -> None:
    """
    Creates a box plot of semantic similarity scores by class, saves it as PNG.

    Args:
        data: A Pandas DataFrame containing columns 'class' and 'semantic_similarity'.
        save_dir: The directory where the plot should be saved.
        plot_width: Width of the plot in inches (default: 10).
        plot_height: Height of the plot in inches (default: 8).
    """
    try:
        # Input Validation
        for col in ['class', 'semantic_similarity']:
            if col not in data.columns:
                raise ValueError(f"Required column '{col}' not found in DataFrame.")
        
        # Prepare data for plotting
        classes = data['class'].unique()
        similarity_data = [data[data['class'] == c]['semantic_similarity'] for c in classes]

        # Create save directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Chart Creation with Matplotlib
        plt.figure(figsize=(plot_width, plot_height))  # Set figure size
        plt.boxplot(similarity_data, labels=classes)
        plt.xlabel('Class')
        plt.ylabel('Semantic Similarity')
        plt.title('Semantic Similarity by Class')
        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for readability

        # Save Plot
        png_save_path = os.path.join(save_dir, 'semantic_similarity_by_class_boxplot.png')
        plt.savefig(png_save_path, bbox_inches='tight')  # Save with tight layout

        logger.info(f"Box plot saved as PNG: {png_save_path}")

    except ValueError as ve:
        logger.error(f"Invalid input: {ve}")
    except Exception as e:
        logger.error(f"Error creating or saving box plot: {e}")


if __name__ == "__main__":
    try:
        # Load data
        data_path = './data/eval/generation/summarized_answers_filtered_results.csv'
        df = pd.read_csv(data_path)
    
        # Save plots
        save_directory = "./data/plots"
        create_semantic_similarity_boxplot(df, save_directory)
        
    except FileNotFoundError:
        logger.error(f"Data file not found at: {data_path}")
    except pd.errors.EmptyDataError:
        logger.error(f"No data found or empty data in: {data_path}") 
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
