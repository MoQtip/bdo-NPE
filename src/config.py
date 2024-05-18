# config.py

# Path to the Excel file containing the game's node data. This file is central to the application's functionality,
# serving as the primary data source for node information.
EXCEL_FILE_PATH = "../data/BDO_database.xlsx"

# Path to the configuration file. This file is used for the application seamless saving functionality.
CONFIG_FILE = "../data/config.json"

# The name of the sheet within the Excel file that contains all relevant node data. Set to None as the entire
# file is used without specifying a particular sheet.
SHEET_NAME_ALL = None

# A string listing the names of yields separated by commas. These yields are targeted by the application for
# optimization and analysis.
YIELD_NAMES = "Potato, Wheat, Rice"

# Directory and filename settings for storing and accessing the HTML visualization of results. This allows users
# to view the optimization results in a more interactive and visually appealing format.
OUTPUT_DIRECTORY = "../output"
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