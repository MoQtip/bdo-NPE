# config.py
import os
import sys
import logging
from collections import namedtuple

# Define a namedtuple to hold the base path and its source
BasePathInfo = namedtuple('BasePathInfo', ['base_path', 'source'])

def setup_logging():
    if '--log' in sys.argv:
        logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info('Logging started')
        log_base_path_info()
    else:
        # Disable all logging if --log is not provided
        logging.basicConfig(level=logging.CRITICAL)

# Function to get the base path (the directory of the executable or script)
def get_base_path():
    """ Get the base path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
        source = f'sys._MEIPASS'
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        source = f'local._NPE'
    return BasePathInfo(base_path=base_path, source=source)

# Function to get the absolute path to a resource
def resource_path(relative_path):
    """ Get the absolute path to a resource """
    base_path_info = get_base_path()
    return os.path.join(base_path_info.base_path, relative_path)

# Function to log base path info
def log_base_path_info():
    base_path_info = get_base_path()
    logging.debug(f'BASE_PATH is: {base_path_info.base_path}')
    logging.debug(f'BASE_PATH_SOURCE is: {base_path_info.source}')

# Path to the Excel file containing the game's node data. This file is central to the application's functionality,
# serving as the primary data source for node information.
EXCEL_FILE_PATH = resource_path(r"data\BDO_database.xlsx")

# Path to the configuration file. This file is used for the application seamless saving functionality.
CONFIG_FILE = resource_path(r"data\config.json")

# The name of the sheet within the Excel file that contains all relevant node data. Set to None as the entire
# file is used without specifying a particular sheet.
SHEET_NAME_ALL = None

# A string listing the names of yields separated by commas. These yields are targeted by the application for
# optimization and analysis.
YIELD_NAMES = "Potato, Wheat, Rice"

# Directory and filename settings for storing and accessing the HTML visualization of results. This allows users
# to view the optimization results in a more interactive and visually appealing format.
OUTPUT_DIRECTORY = resource_path("output")
DEFAULT_HTML_FILE_NAME = "results_visualization.html"

# Configuration for opening the HTML output in a new tab of the web browser, enhancing user experience by
# providing immediate access to the visualization.
WEBBROWSER_NEW_TAB = 2

# Specific Excel sheet names within the NodeProcessor module. These are utilized for detailed processing
# and analysis of nodes, their connections, and yields.
SHEET_WORKERS_LODGING = "Worker's Lodging"
SHEET_NODES_NAME_REGION = "Nodes Name & Region"
SHEET_NODE_CONNECTIONS = "Node Connections"
SHEET_NODE_YIELDS = "Node Yields"

# Column names used in DataFrame operations throughout the application. These constants ensure consistency
# and reduce the risk of errors in data manipulation.
COLUMN_AVAILABLE = "Available"
COLUMN_NODE_ID = "Node ID"
COLUMN_TOTAL_LODGING_CP_COST = "Total Lodging CP Cost"
COLUMN_LODGING_NAME = "Lodging Name"
COLUMN_NODE_TYPE = "Node Type"
COLUMN_YIELD_1 = "Yield 1"
COLUMN_YIELD_2 = "Yield 2"
COLUMN_CONNECTED = "Connected"
COLUMN_CP_COST = "CP Cost"
COLUMN_NODE_NAME = "Node Name"

# Definitions of node types and identifiers used in logic for processing nodes, specifically focusing on
# cities and towns due to their significance in the game.
NODE_TYPES_CITY_TOWN = ["City", "Town"]
CONNECTED_NODE_ID = "Connected Node ID"

# Default values used in the application, particularly for scenarios where specific lodging information
# is not available or applicable.
DEFAULT_NO_LODGING_NAME = "No Lodging"
DEFAULT_NO_LODGING_CP_COST = 0