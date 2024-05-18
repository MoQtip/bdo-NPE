import sys
from data_loader import ExcelDataLoader
from node_processor import NodeProcessor
from results_visualizer import ResultsVisualizer
import config

def sanitize_yield_names(yield_names):
    """Convert comma-separated string to a set of normalized (stripped, lowercased) yield names."""
    return {name.strip().lower() for name in yield_names.split(',')}

if __name__ == "__main__":
    # Check for command-line arguments; if provided, use these, otherwise use config.YIELD_NAMES.
    if len(sys.argv) > 1:
        input_yield_names = sys.argv[1]
        normalized_yield_names = sanitize_yield_names(input_yield_names)
    else:
        normalized_yield_names = sanitize_yield_names(config.YIELD_NAMES)

    # Convert the set back to a sorted comma-separated string and update config.YIELD_NAMES.
    config.YIELD_NAMES = ', '.join(sorted(normalized_yield_names))

    # Load node data from the Excel file specified in the application's configuration.
    loader = ExcelDataLoader(config.EXCEL_FILE_PATH)
    excel_sheets_data = loader.load_excel_data()
    
    # Process the loaded node data to calculate optimal paths and CP investments for specified yields.
    processor = NodeProcessor(excel_sheets_data)
    all_yield_results = processor.process_nodes(config.YIELD_NAMES)

    # Output the processed node data and analysis results to the console and an HTML file for easy viewing.
    ResultsVisualizer.print_console_output(all_yield_results)

    # Generate and save an HTML file containing the visualized results, and open it in a web browser.
    html_output = ResultsVisualizer.generate_html_output(all_yield_results)
    ResultsVisualizer.save_and_open_html(html_output)
