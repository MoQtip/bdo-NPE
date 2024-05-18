import sys
import os
import ctypes
import json
import webbrowser
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog, QDesktopWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import config
from data_loader import ExcelDataLoader
from node_processor import NodeProcessor
from results_visualizer import ResultsVisualizer

class NodePathExplorerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'BDO Node Path Explorer (v1.0.0)'
        self.initUI()
        self.loadSettings()

    def initUI(self):
        # Initialize the main window and its UI elements
        self.setWindowTitle(self.title)
        self.setFixedSize(640, 480)
        self.centerWindow()
        self.setWindowIcon(QIcon('../assets/app_icon.ico'))
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()

        # Initialize Excel file path components
        self.excelFileLabel = QLabel("Excel File Path:")
        self.layout.addWidget(self.excelFileLabel)
        self.excelFilePathLineEdit = QLineEdit(self)
        default_excel_path = os.path.abspath(config.EXCEL_FILE_PATH)

        self.excelFilePathLineEdit.setText(default_excel_path)
        self.layout.addWidget(self.excelFilePathLineEdit)

        # Button to open a dialog for selecting Excel files
        self.excelFilePickerButton = QPushButton('Select Excel File')
        self.excelFilePickerButton.clicked.connect(self.openFileNameDialog)
        self.styleButton(self.excelFilePickerButton)
        self.layout.addWidget(self.excelFilePickerButton)

        # Initialize Yield Names input
        self.yieldNamesLabel = QLabel("Yield Names (comma-separated):")
        self.layout.addWidget(self.yieldNamesLabel)
        self.yieldNamesTextEdit = QTextEdit(self)
        self.yieldNamesTextEdit.setPlaceholderText("Enter yield names, separated by commas")
        self.layout.addWidget(self.yieldNamesTextEdit)

        # Button to process data
        self.processButton = QPushButton('Process Data')
        self.processButton.clicked.connect(self.processData)
        self.styleButton(self.processButton)
        self.layout.addWidget(self.processButton)

        # Button to open results visualization in a web browser
        self.openHTMLButton = QPushButton('Open Results Visualization')
        self.openHTMLButton.clicked.connect(self.openResultsVisualization)
        self.styleButton(self.openHTMLButton)
        self.layout.addWidget(self.openHTMLButton)

        # Auto-save settings when text fields change
        self.excelFilePathLineEdit.textChanged.connect(self.saveSettings)
        self.yieldNamesTextEdit.textChanged.connect(self.saveSettings)

        self.centralWidget.setLayout(self.layout)

    def centerWindow(self):
        # Center the application window on the screen
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFileNameDialog(self):
        # Open a file dialog to select an Excel file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            self.excelFilePathLineEdit.setText(fileName)

    def processData(self):
        # Process data using the specified Excel file and Yield names, normalize and sort yield names
        excel_file_path = self.excelFilePathLineEdit.text()
        yield_names = self.yieldNamesTextEdit.toPlainText().strip()
        if not yield_names:
            # Normalize and sort yield names from config if no GUI input
            yield_names = ', '.join(sorted({name.strip().lower() for name in config.YIELD_NAMES.split(',')}))
        else:
            # Normalize and sort yield names from GUI input
            yield_names = ', '.join(sorted({name.strip().lower() for name in yield_names.split(',')}))

        if excel_file_path:
            config.EXCEL_FILE_PATH = excel_file_path
            config.YIELD_NAMES = yield_names
            loader = ExcelDataLoader(excel_file_path)
            excel_sheets_data = loader.load_excel_data()
            processor = NodeProcessor(excel_sheets_data)
            all_yield_results = processor.process_nodes(yield_names)
            ResultsVisualizer.print_console_output(all_yield_results)
            html_output = ResultsVisualizer.generate_html_output(all_yield_results)
            ResultsVisualizer.save_and_open_html(html_output)
            print("Data processing complete.")
        else:
            print("Please select an Excel file and enter yield names.")

    def openResultsVisualization(self):
        # Open the results visualization in the default web browser
        absolute_file_path = os.path.abspath(os.path.join(config.OUTPUT_DIRECTORY, config.DEFAULT_HTML_FILE_NAME))
        webbrowser.open_new_tab(f'file://{absolute_file_path}')

    def styleButton(self, button):
        # Apply styling to buttons
        button.setStyleSheet("QPushButton { background-color: #2596be; color: white; }"
                             "QPushButton::hover { background-color: #34a1eb; }")

    def saveSettings(self):
        # Save settings to a JSON file whenever text changes
        settings = {
            'excelFilePath': self.excelFilePathLineEdit.text(),
            'yieldNames': self.yieldNamesTextEdit.toPlainText()
        }
        with open(config.CONFIG_FILE, 'w') as config_file:
            json.dump(settings, config_file)

    def loadSettings(self):
        # Load settings from a JSON file or set default values
        try:
            with open(config.CONFIG_FILE, 'r') as config_file:
                settings = json.load(config_file)
                self.excelFilePathLineEdit.setText(settings.get('excelFilePath', config.EXCEL_FILE_PATH))
                self.yieldNamesTextEdit.setText(settings.get('yieldNames', ''))

        except FileNotFoundError:
            self.excelFilePathLineEdit.setText(config.EXCEL_FILE_PATH)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../assets/app_icon.ico'))
    myappid = 'com.moqtip.NodePathExplorer.1'  # Unique identifier for the application
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ex = NodePathExplorerGUI()
    ex.show()
    sys.exit(app.exec_())