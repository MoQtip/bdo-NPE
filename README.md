<h1 align="center" style="display: block; font-size: 2.5em; font-weight: bold; margin-block-start: 1em; margin-block-end: 1em;">
<a name="logo"><img align="center" src="https://github.com/MoQtip/bdo-NPE/blob/moqtip/assets/npe_logo_20%25.png" alt="BDO NodePath Explorer (NPE)"/></a>
  <br /><br /><strong>BDO NodePath Explorer (NPE)</strong>
</h1>

<p align="justify"> The "BDO NodePath Explorer" (NPE) application is designed to optimize node management in the MMORPG "Black Desert Online" (BDO). It assists players in planning and strategizing their in-game node investments by calculating optimal paths and minimizing Contribution Points (CP) costs. By analyzing node connections, types, and yields, the application provides actionable insights into how players can efficiently manage their node networks for gathering resources, trading, or other economic activities within BDO.</p>

---

## Table of Contents

1. [Introduction](#1-introduction)
   - [Target Audience](#small_red_triangle_down-target-audience)
   - [How It Helps](#small_red_triangle_down-how-it-helps)
2. [Getting Started](#2-getting-started)
   - [Installation](#small_red_triangle_down-installation)
   - [Quick Start Guide](#small_red_triangle_down-quick-start-guide)
3. [Architecture and Design](#3-architecture-and-design)
   - [High-Level Overview](#small_red_triangle_down-high-level-overview)
   - [Design Choices](#small_red_triangle_down-design-choices)
   - [Interactions Between Components](#small_red_triangle_down-interactions-between-components)
4. [Usage Examples](#4-usage-examples)
   - [Analyzing Specific Node Paths](#small_red_triangle_down-analyzing-specific-node-paths)
   - [Optimizing for Multiple Yields](#small_red_triangle_down-optimizing-for-multiple-yields)
   - [Tips and Tricks](#information_source-tips-and-tricks)
   - [Visualization Tips](#information_source-visualization-tips)
5. [Detailed Excel Database Documentation](#5-detailed-excel-database-documentation)
   - [Overview](#small_red_triangle_down-overview)
   - [Sheet Details and Column Significance](#small_red_triangle_down-sheet-details-and-column-significance)
6. [Contributing](#6-contributing)
   - [Guidelines](#small_red_triangle_down-guidelines)
   - [Issue Reporting](#small_red_triangle_down-issue-reporting)
   - [Known Limitations or Challenges](#small_red_triangle_down-known-limitations-or-challenges)
7. [Changelog and Versioning](#7-changelog-and-versioning)
   - [Changelog](#small_red_triangle_down-changelog)
   - [Versioning](#small_red_triangle_down-versioning)
8. [Credits and Acknowledgments](#8-credits-and-acknowledgments)
   - [BDOLytics](#small_red_triangle_down-bdolytics)
   - [Workerman](#small_red_triangle_down-workerman)
   - [Community Contributions](#small_red_triangle_down-community-contributions)

---

## 1: Introduction

### :small_red_triangle_down: Target Audience

This application is geared towards a wide range of BDO players, including:

- **New Players:** Those who are just starting out and need guidance on how to effectively use their CP in node investments.
- **Veteran Players:** Seasoned players looking to refine their node management strategies for better resource optimization or to expand their trading networks.
- **Economy-Focused Players:** Individuals particularly interested in the economic aspects of BDO, such as trading and resource gathering, who want to maximize their in-game profits.
- **Guild Leaders and Members:** Players involved in managing guild resources can utilize this tool to plan and optimize guild-wide node investments.

### :small_red_triangle_down: How It Helps

The "BDO NodePath Explorer" simplifies the complex process of node management by providing:

- **Data-Driven Insights:** Utilizes up-to-date node data to offer recommendations on which nodes to invest in.
- **CP Optimization:** Identifies the most CP-efficient paths for connecting nodes, allowing players to save CP for other investments.
- **Yield Maximization:** Helps players target nodes that offer specific yields, enhancing resource gathering and trading strategies.
- **Visual Path Analysis:** Offers an intuitive visualization of node networks, making it easier to plan and adjust strategies.

**:information_source: Tips:** By using the "BDO NodePath Explorer", players can make informed decisions, saving time and in-game resources, thereby enhancing their gameplay experience in "Black Desert Online."

---

## 2: Getting Started

This section provides all the necessary information to install and start using the "BDO NodePath Explorer" application quickly.

### :small_red_triangle_down: Installation

Before you begin, ensure you have Python installed on your system as the application is developed in Python. Python 3.8 or newer is recommended. You will also need Pandas library for data manipulation and a few other libraries depending on the features you wish to use.

1. **Download the Application:** First, download the application files from the repository. You can clone the repository using Git or download the files directly as a ZIP archive and extract them on your machine.

  ```bash
  git clone https://github.com/MoQtip/bdo-NPE.git
  ```

2. **Install Dependencies:** Navigate to the application directory and install the required Python libraries using pip. The requirements.txt file in the application's root directory lists all the necessary dependencies.

  ```bash
  cd <root folder>
  pip install -r requirements.txt
  ```

### :small_red_triangle_down: Quick Start Guide

Once the installation is complete, you're ready to start optimizing your node paths in "Black Desert Online". Here's how to get started:

1. **Prepare the Node Data Excel File:** Make sure you have the BDO_database.xlsx file ready. This file should contain the latest node data. By default, the application expects this file to be in the root directory of the project.

    - Modify the config.py file by updating the EXCEL_FILE_PATH to indicate the exact location of your Excel file, using an absolute path. Additionally, adjust the YIELD_NAMES in the same file to replace the default values with your desired yields, separated by commas.
    - Furthermore, based on your progress in the game, update the 'Connected' and 'Available' columns in the 'Nodes Name & Region' and 'Worker's Lodging' sheets, respectively. If you are a newcomer to the game, leave these columns as they are.

2. **Run the Application:** Execute main.py to start the application. This script orchestrates the loading of node data, processing of nodes based on specified yields, and visualization of results.

  ```bash
  python main.py
  ```

3. **Review the Results:** After running the application, check the console output for a summary of the results. Additionally, an HTML file with a detailed visualization of the node paths and CP investments will be generated and automatically opened in your default web browser. The results will provide insights into the most CP-efficient paths and suggest which nodes to invest in for optimizing your desired yields.

**:information_source: Tips:** Alternatively, you can execute the following module to bypass editing config.py and access a basic, yet functional GUI:

  ```bash
  cd <root folder/src>
  python npe_gui.py
  ```

---

## 3: Architecture and Design

This section provides a detailed look at the architecture and design of the "BDO NodePath Explorer" application, explaining how its components work together to deliver its functionality.

### :small_red_triangle_down: High-Level Overview

The "BDO NodePath Explorer" application is structured into several key Python modules, each responsible for a distinct aspect of the application's functionality. At a high level, the application can be understood as consisting of the following components:

- **Data Loader (data_loader.py):** Responsible for loading and preparing the node data from an Excel file. This component ensures that the data is in a format that can be easily processed and analyzed by the application.
  
- **Node Processor (node_processor.py):** The core logic of the application resides here. This component processes the loaded node data to calculate optimal paths between nodes and the minimum CP investments required, based on specified yields.
  
- **Results Visualizer (results_visualizer.py):** Handles the presentation of the processed node data, including printing results to the console and generating an HTML visualization of the node paths and CP investments.
  
- **Configuration (config.py):** Contains configuration settings for the application, such as paths to the Excel data file, sheet names, and other constants used throughout the application.
  
- **Main Script (main.py):** Serves as the entry point to the application. It orchestrates the flow from data loading, processing, to visualization of results.

- **GUI (npe_gui.py):** Manages the Graphical User Interface (GUI), handling user interactions, visual displays, and integration of user input with backend processing.

### :small_red_triangle_down: Design Choices

- **Python:** The choice of Python as the programming language was driven by its rich ecosystem of data analysis and manipulation libraries, such as Pandas, which greatly simplify the handling of complex data structures and computational tasks involved in this application.
  
- **Pandas for Data Manipulation:** Pandas is used extensively for its powerful data manipulation capabilities, enabling efficient processing of node data for analysis.
  
- **Modular Design:** The application is designed with modularity in mind, separating concerns into different modules. This approach enhances maintainability, makes the codebase easier to navigate, and simplifies the addition of new features or updates.

### :small_red_triangle_down: Interactions Between Components

- **Initialization:** The main.py or npe_gui.py scripts start the application, first invoking the Data Loader to fetch and prepare the node data.
  
- **Data Processing:** With the data loaded, the Node Processor takes over to analyze the node data against the application's logic, calculating optimal node connections and CP investments.
  
- **Result Visualization:** Once processing is complete, the Results Visualizer presents the findings to the user, both through the console and an HTML document for a more interactive experience.

---

## 4: Usage Examples

In this section, I provide practical examples of how to use the "BDO NodePath Explorer" application to address more complex scenarios and optimize your gameplay in "Black Desert Online". These examples are designed to demonstrate the application's capabilities beyond basic operations, offering insights into its versatility and power.

### :small_red_triangle_down: Example 1: Analyzing Specific Node Paths

**Scenario:** You want to determine the most CP-efficient path to connect a specific set of nodes for a particular resource yield.

**Steps:**

1. **Identify Target Yield:** Determine the specific resource yield you're targeting.
2. **Update Configuration: (ignore if you run npe_gui.py)** Modify the `config.py` file to include your targeted yield.
3. **Run the Application:** Execute `main.py` or `npe_gui.py` to process the node data based on your specified criteria.
4. **Review Results:** Analyze the output in the console and the generated HTML file to understand the recommended node connections and CP investments.

**Example Usage:**

```python
# Update the YIELD_NAMES in config.py to include multiple targets
# For example, YIELD_NAMES = "Flax Thread"
python main.py
# or use the GUI script to bypass editing config.py
python npe_gui.py
```

### :small_red_triangle_down: Example 2: Optimizing for Multiple Yields

**Scenario:** You aim to optimize your node network to efficiently gather multiple types of resources while minimizing CP usage.

**Steps:**

1. **Specify Multiple Yields:** List the resource yields you're interested in optimizing for in the `config.py` file, separated by commas.
3. **Update Configuration: (ignore if you run npe_gui.py)** Modify the `config.py` file to include your targeted yields.
3. **Process Node Data:** Execute `main.py` or `npe_gui.py` to process the node data based on your specified criteria.
4. **Evaluate Recommendations:** Use the detailed results to plan your node investments and connections, focusing on areas that offer the best Total CP cost for your specified yields.

**Example Usage:**

```python
# Update the YIELD_NAMES in config.py to include multiple targets
# For example, YIELD_NAMES = "Wheat, Copper Ore, Maple Timber"
# Then, execute the application
python main.py
# or use the GUI script to bypass editing config.py
python npe_gui.py
```

**:information_source: Tips and Tricks**

- **Advanced Analysis:** Consider using the results in conjunction with other BDO tools or resources, such as marketplace data or guild requirements, for more comprehensive strategy planning.

**:information_source: Visualization Tips**

- **Sharing Results:** The HTML visualization can be shared with guild members or friends to collaborate on node investment strategies, enhancing teamwork and in-game efficiency.

---

## 5: Detailed Excel Database Documentation

### :small_red_triangle_down: Overview

The Excel database is integral to the BDO NodePath Explorer, organizing critical information about nodes, their relationships, yields, and worker lodging. This data underpins the application’s functionality by allowing strategic planning and real-time adjustments based on gameplay dynamics.

### :small_red_triangle_down: Sheet Details and Column Significance

#### :black_small_square: Nodes Name & Region
- **Node ID** (Primary Key): Uniquely identifies each node, linking all related data across the database.
- **Node Name**: The name of the node as it appears in the game.
- **Node Region**: Categorizes nodes by their geographical or logical region, important for regional strategy considerations.
- **Connected** `(User-modifiable)`: A boolean indicating whether the node is currently connected or active, enabling resource and contribution benefits associated with that node.
- **Node Type**: Classifies nodes by their operational type (e.g., resource, military), influencing decision-making.
- **CP Cost**: Shows the Contribution Points required to activate or maintain a node, crucial for resource management.
- **Node Manager**: Names the NPC responsible for the node, adding a layer of interaction and narrative.

#### :black_small_square: Sheet: Node Connections
- **Connection ID**: Serves as a unique identifier for each node connection entry.
- **Node ID**: Identifies the node from which a connection originates, critical for mapping network strategies.
- **Connected Node ID**: Identifies the node at the connection’s end, essential for understanding and visualizing the node network.

#### :black_small_square: Sheet: Node Yields
- **Yield ID**: A unique identifier for each yield record, important for tracking and inventory purposes.
- **Node ID**: Connects yields to their respective nodes, crucial for operational planning.
- **Yield 1**, **Yield 2**: Detailed descriptions of specific yields from the node, vital for optimizing resource allocation and strategy.

#### :black_small_square: Sheet: Worker's Lodging
- **Lodging ID**: Uniquely identifies lodging options within nodes.
- **Node ID**: Associates each lodging option with a specific node, crucial for logistical planning.
- **Lodging Name**: Descriptive name of the lodging, important for specific identification and user interaction.
- **CP Cost**: Indicates the Contribution Points cost of lodging, key for budgeting and planning.
- **Parent Lodging**: Identifies any superior lodging that this entry depends on, important for understanding lodging hierarchies.
- **Parent CP Cost**: Shows the CP cost of the parent lodging, essential for cumulative budgeting.
- **Total Lodging CP Cost**: Aggregates CP costs for this lodging, taking parent costs into account.
- **Number of Workers**: Indicates the capacity of workers that can be housed, critical for workforce management.
- **Available** `(User-modifiable)`: Shows whether the lodging is currently available for use.

#### :black_small_square: Sheet: Lodging Usages
- **Node ID**: Links usage options to their respective nodes, fundamental for operational planning.
- **Lodging Name**: Identifies the specific lodging space.
- **CP Cost**, **Parent Lodging**, **Parent CP Cost**, **Total Lodging CP Cost**: These columns are crucial for understanding and managing the costs associated with each lodging space.
- **Usage 1** to **Usage 7**: Define potential applications of each lodging space, critical for maximizing space utilization and strategic planning.

**:information_source: User Interaction**

Users can interact with the Excel file primarily through modifications to the `Connected` (Nodes Name & Region) and `Available` (Worker's Lodging) columns, which directly impact the operational state of nodes and lodging availability. The provided descriptions are provided to ensure that users make these modifications responsibly and in alignment with thier overall game strategy.

---

## :trophy: 6: Contributing

The "BDO NodePath Explorer" application welcomes contributions from the community. Whether you're fixing bugs, adding new features, or improving documentation, your help can make the application even better for everyone. Here's how you can contribute:

### :small_red_triangle_down: Guidelines

**Setting Up Your Development Environment:**

1. **Fork the Repository:** Start by forking the application repository to your GitHub account. This creates a personal copy for you to work on.
2. **Clone Your Fork:** Clone your forked repository to your local machine to start making changes.
 ```bash
 git clone https://github.com/MoQtip/bdo-NPE.git
 ```
3. **Install Dependencies:** Navigate to the project directory and install the required dependencies.
 ```bash
 pip install -r requirements.txt
 ```

**Making Changes:**

1. **Create a New Branch:** For each set of changes or new feature, create a new branch off the main project.
   ```bash
   git checkout -b feature/my-new-feature
   ```
2. **Implement Your Changes:** Make your changes, ensuring they are well-documented and follow the project's coding standards.
3. **Test Your Changes:** Run any existing tests, and write new ones if necessary, to ensure your changes don't break existing functionality.
4. **Commit Your Changes:** Commit your changes with a clear, descriptive message. Include any relevant issue numbers in your commit message.
 ```bash
 git commit -am 'Add some feature #123'
 ```

**Submitting Your Contributions:**

1. **Push to GitHub:** Push your branch to your GitHub fork.
 ```bash
 git push origin feature/my-new-feature
 ```
2. **Open a Pull Request:** Navigate to the original repository on GitHub, and you'll see a prompt to open a pull request from your new branch. Fill out the pull request form with a clear description of your changes and any other relevant information.
3. **Review & Merge:** Your pull request will be reviewed by the maintainers, and if approved, merged into the main project.

### :small_red_triangle_down: Issue Reporting

If you encounter any bugs or have suggestions for new features or improvements, please report them by opening an issue in the GitHub repository. Be as detailed as possible in your description, providing steps to reproduce the bug or outlining your feature request clearly.

### :small_red_triangle_down: Known Limitations or Challenges

- I strive to make the "BDO NodePath Explorer" as robust and user-friendly as possible, but there may be limitations or known issues. Contributing towards addressing these can significantly benefit the community. Check the GitHub issues section to see if there are known challenges you might help resolve.

- *Microsoft SmartScreen Alert*: When downloading the packaged `.exe` file of this application, Windows might display an alert from the Microsoft SmartScreen filter. This is a security measure for applications from unknown publishers. As a free offering, this app isn't signed with a digital certificate due to the high costs involved. You can safely proceed by clicking "More info" and then "Run anyway" to start the app.

- *Checksum Verification*: For added security, a checksum of the `.exe` file is provided to verify the integrity of the download. After downloading the file, you can use a tool like `certUtil` on Windows to compare the provided checksum against the downloaded file’s checksum. This step helps ensure that the file has not been altered or corrupted. Here's a quick example on how to use certUtil to verify a checksum:
 ```bash
 certUtil -hashfile bdo_npe.exe SHA256
 ```

---

## 7: Changelog and Versioning

Maintaining a detailed changelog and adhering to a consistent versioning strategy are critical practices for the ongoing development and user support of the "BDO NodePath Explorer" application. These practices ensure that contributors and users alike are informed about the evolution of the software, understanding what changes have been made and how they might affect usage or development.

### :small_red_triangle_down: Changelog

The changelog is a record of all notable changes made to the project, organized by version. It should be easy to read and understand, providing a clear history of the project's development. The changelog for "BDO NodePath Explorer" is maintained in the `CHANGELOG.md` file at the root of the project repository.

**Updating the Changelog:**

**New Entries:** Whenever a new version is released, a new entry is added to the `CHANGELOG.md` file detailing the changes made since the last version. This includes new features, bug fixes, performance improvements, and any breaking changes.

**Structure:** The changelog is structured by version numbers, with the most recent version at the top. Each version section should include the release date and a list of changes categorized by type.

**Contribution:** Contributors are encouraged to include changelog entries with their pull requests when applicable. This practice helps to ensure that the changelog remains up-to-date and accurate.

**Example Changelog Entry:**

```markdown
## [1.2.0] - 2024-04-01
### Added
- New algorithm for optimizing node paths to reduce CP cost.
- HTML output now includes interactive node maps.

### Fixed
- Corrected issue where certain node types were incorrectly processed.

### Changed
- Updated data_loader module to improve Excel file handling performance.
```

### :small_red_triangle_down: Versioning

The "BDO NodePath Explorer" application follows Semantic Versioning (SemVer) principles. This means that version numbers are assigned in the format of MAJOR.MINOR.PATCH:

- MAJOR version when making incompatible API changes,
- MINOR version when adding functionality in a backward-compatible manner, and
- PATCH version when making backward-compatible bug fixes.

**Versioning Strategy:**

**Releases:** New versions are released after a significant set of changes have been accumulated or an important feature or fix has been implemented.

**Pre-releases and Builds:** For larger changes or features under development, pre-release versions or build tags may be used for testing purposes.

**Tagging:** Each release is tagged in the repository, correlating with the version number and providing a snapshot of the code at the point of release.

**Example Versioning:**

- Initial release: 1.0.0
- Subsequent minor feature addition: 1.1.0
- Patch release for a bug fix: 1.1.1

---

## :handshake: 8: Credits and Acknowledgments

The "BDO NodePath Explorer" application has been inspired by and benefited from the existing knowledge base and tools available to the "Black Desert Online" community. I would like to extend my heartfelt thanks and acknowledge the contributions of the following resources and applications:

### :small_red_triangle_down: BDOLytics
- **Website:** [BDOLytics](https://bdolytics.com/en/NA)

BDOLytics has been an invaluable resource for understanding the intricacies of "Black Desert Online's" economy and node system. The comprehensive data and insights provided by BDOLytics have greatly influenced the development of the "BDO NodePath Explorer," especially in terms of data analysis and the application's approach to node management optimization.

### :small_red_triangle_down: Workerman
- **Website:** [Workerman](https://shrddr.github.io/workerman/plantzones)

The Workerman tool has offered significant inspiration in the visualization of node networks and the implementation of efficient pathfinding algorithms. The methodologies applied in Workerman for managing worker assignments and node connections have been instrumental in shaping the algorithms and user interface design of the "BDO NodePath Explorer."

### :small_red_triangle_down: Community Contributions
The development of the "BDO NodePath Explorer" has also been fueled by the vibrant "Black Desert Online" community. Player insights, feedback, and shared strategies have been crucial in tailoring the application to meet the needs of BDO players. I am grateful for the community's support and enthusiasm, which continue to drive the application's evolution.
