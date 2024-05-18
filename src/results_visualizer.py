import os
import webbrowser
import html
import config

class ResultsVisualizer:
    """
    Provides functionality for visualizing node processing results, both in the console and as an HTML document.
    """

    @staticmethod
    def print_console_output(all_yield_results):
        """
        Prints the node processing results for each yield to the console.
        
        Parameters:
            all_yield_results (list): A list of tuples, each containing a yield name and a DataFrame with the results for that yield.
        """
        for yield_name, node_results_dataframe in all_yield_results:
            print(f"Node Processing Results for Yield: {yield_name}\n")
            print(node_results_dataframe.to_string(index=False), "\n")

    @staticmethod
    def generate_html_output(all_yield_results):
        """
        Generates an HTML document string that visualizes the node processing results.

        Parameters:
            all_yield_results (list): A list of tuples, each containing a yield name and a DataFrame with the results for that yield.

        Returns:
            str: A string containing the HTML document for visualizing the results.
        """
        html_output = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BDO NodePath Explorer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .tab { overflow: hidden; border: 1px solid #ccc; background-color: #f1f1f1; }
            .tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 16px; transition: 0.3s; }
            .tab button:hover { background-color: #ddd; }
            .tab button.active { background-color: #ccc; }
            .tabcontent { display: none; padding: 6px 12px; border: 1px solid #ccc; border-top: none; }
            .table { width: 100%; border-collapse: collapse; }
            .table, .table th, .table td { border: 1px solid black; }
            .table th, .table td { text-align: left; padding: 8px; }
            .table th { background-color: #f2f2f2; }
            .highlight { background-color: lightblue; } /* CSS class for highlighting */
            ul { padding-left: 20px; } /* Style for bullet points */
            li { margin-bottom: 5px; } /* Space between items */
        </style>
    </head>
    <body>

    <div class='tab'>
    """
        for yield_name, _ in all_yield_results:
            escaped_yield_name = html.escape(yield_name)  # Escape special characters in yield names
            html_output += f"<button class='tablinks' onclick='openYield(event, \"{escaped_yield_name}\")'>{escaped_yield_name}</button>\n"
        html_output += "</div>\n"

        html_output += """
    <script>
    function openYield(evt, yieldName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(yieldName).style.display = "block";
    evt.currentTarget.className += " active";
    highlightCP(); /* Call highlight function whenever a tab is opened */
    }
    </script>
    """

        for yield_name, node_results_dataframe in all_yield_results:
            escaped_yield_name = html.escape(yield_name)  # Escape special characters in yield names
            # Disabling escaping for the whole table and manually escaping other content
            html_table = node_results_dataframe.to_html(index=False, escape=False, classes="table", border=0, formatters={
                "Visited Nodes Info": lambda x: '<ul>' + ''.join(f'<li>{item.strip()}</li>' for item in x.split(',')) + '</ul>'
            })
            html_output += f"<div id='{escaped_yield_name}' class='tabcontent'><h3>{escaped_yield_name}</h3>{html_table}</div>\n"

        html_output += """
    <script>
    document.getElementsByClassName('tablinks')[0].click(); // Activate the first tab initially

    function highlightCP() {
        var regex = /(?:^|<li>)([^<]*?\\(ID: \\d+ - CP: \\*0\\.0 CP\\))/g; // Updated regex for list items
        var ulElements = document.querySelectorAll('.table ul');
        ulElements.forEach(function(ul) {
            var liElements = ul.children;
            for (let li of liElements) {
                var match = regex.exec(li.innerHTML);
                if (match) {
                    li.classList.add('highlight');
                }
                regex.lastIndex = 0; // Reset regex after each check
            }
        });
    }
    window.onload = highlightCP;
    </script>
    </body>
    </html>
    """
        return html_output

    @staticmethod
    def save_and_open_html(html_output, file_name=config.DEFAULT_HTML_FILE_NAME):
        """
        Saves the generated HTML output to a file and opens it in a web browser.
        
        Parameters:
            html_output (str): The HTML document as a string.
            file_name (str, optional): The name of the file to save the HTML document as. Defaults to config.DEFAULT_HTML_FILE_NAME.
        """
        output_directory = os.path.abspath(config.OUTPUT_DIRECTORY)
        file_path = os.path.join(output_directory, file_name)
        
        # Create the output directory if it doesn't exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Save the HTML content to the file
        with open(file_path, "w") as f:
            f.write(html_output)
        
        # Open the file in the default web browser
        webbrowser.open("file://" + file_path, new=config.WEBBROWSER_NEW_TAB)  # new=2 opens in a new tab, if possible
