import pandas as pd
import config

class NodeProcessor:
    """
    Processes node data to calculate optimal paths and Contribution Points (CP) investments based on specified yields.
    
    Attributes:
        excel_sheets_data (DataFrame): A DataFrame containing the loaded node data from an Excel file.
    """

    def __init__(self, excel_sheets_data):
        """
        Initializes the NodeProcessor with node data.
        
        Parameters:
            excel_sheets_data (DataFrame): Node data loaded from an Excel file.
        """
        self.excel_sheets_data = excel_sheets_data

    def get_min_lodging_per_node(self):
        """
        Filters available lodgings and returns the one with the minimum CP cost per node.
        
        Returns:
            DataFrame: A DataFrame of lodgings with the minimum CP cost per node.
        """
        filtered_lodgings_available = self.excel_sheets_data[config.SHEET_WORKERS_LODGING][self.excel_sheets_data[config.SHEET_WORKERS_LODGING][config.COLUMN_AVAILABLE] == True]
        return filtered_lodgings_available.loc[filtered_lodgings_available.groupby(config.COLUMN_NODE_ID)[config.COLUMN_TOTAL_LODGING_CP_COST].idxmin()]

    def merge_nodes_with_lodging(self):
        """
        Merges node information with the minimum lodging CP data to provide a comprehensive view.
        
        Returns:
            DataFrame: A DataFrame containing node information merged with minimum lodging CP costs.
        """
        node_names_and_regions = self.excel_sheets_data[config.SHEET_NODES_NAME_REGION]
        minimum_lodging_cp_costs = self.get_min_lodging_per_node()[[config.COLUMN_NODE_ID, config.COLUMN_LODGING_NAME, config.COLUMN_TOTAL_LODGING_CP_COST, config.COLUMN_AVAILABLE]]
        return pd.merge(node_names_and_regions, minimum_lodging_cp_costs, on=config.COLUMN_NODE_ID, how="left").fillna({config.COLUMN_TOTAL_LODGING_CP_COST: config.DEFAULT_NO_LODGING_CP_COST, config.COLUMN_LODGING_NAME: config.DEFAULT_NO_LODGING_NAME})

    def process_nodes(self, target_yields):
        """
        Processes nodes based on target yields, merging data, and calculating paths and CP investments.
        
        Parameters:
            target_yields (str): A string of target yields separated by commas.
            
        Returns:
            list: A list of tuples, each containing a target yield and its corresponding DataFrame of node results.
        """
        nodes_with_min_lodging_info = self.merge_nodes_with_lodging()
        city_and_town_nodes = nodes_with_min_lodging_info[nodes_with_min_lodging_info[config.COLUMN_NODE_TYPE].isin(config.NODE_TYPES_CITY_TOWN)]
        node_connection_data = self.excel_sheets_data[config.SHEET_NODE_CONNECTIONS]
        
        all_yield_results = []
        for target_yield in map(lambda x: x.strip().lower(), target_yields.split(",")):
            nodes_matching_target_yields = self.excel_sheets_data[config.SHEET_NODE_YIELDS]
            nodes_matching_target_yields = nodes_matching_target_yields[
                nodes_matching_target_yields[[config.COLUMN_YIELD_1, config.COLUMN_YIELD_2]]
                .map(lambda x: str(x).lower() if x is not None else '')
                .isin([target_yield]).any(axis=1)
            ]
            if nodes_matching_target_yields.empty:
                print(f"Warning: Yield '{target_yield.capitalize()}' not found in the Excel sheet. Skipping...")
                continue

            detailed_target_nodes_info = pd.merge(nodes_matching_target_yields, nodes_with_min_lodging_info, on=config.COLUMN_NODE_ID)
            node_processing_results = [self.process_node(node, city_and_town_nodes, node_connection_data, nodes_with_min_lodging_info) for _, node in detailed_target_nodes_info.iterrows()]
            node_results_dataframe = pd.DataFrame(node_processing_results)
            minimum_cp_cost = node_results_dataframe["Total CP"].min()
            results_with_minimum_cp = node_results_dataframe[node_results_dataframe["Total CP"] == minimum_cp_cost]
            all_yield_results.append((target_yield.capitalize(), results_with_minimum_cp))

        return all_yield_results


    def process_node(self, node, city_and_town_nodes, node_connection_data, nodes_with_min_lodging_info):
        """
        Calculates the CP and path for a single node and returns its details.
        
        Parameters:
            node (Series): A Series representing a single node's data.
            city_and_town_nodes (DataFrame): Data for city and town nodes.
            node_connection_data (DataFrame): Data for node connections.
            nodes_with_min_lodging_info (DataFrame): Node data merged with minimum lodging information.
            
        Returns:
            dict: Details of the processed node including ID, name, visited nodes, lodging name, lodging CP, and total CP.
        """
        visited_node_ids, total_path_cp_cost = self.find_path_and_cp(node[config.COLUMN_NODE_ID], city_and_town_nodes, node_connection_data, nodes_with_min_lodging_info)
        selected_lodging_name, selected_lodging_cp_cost = self.get_lodging_details(visited_node_ids, nodes_with_min_lodging_info)
        total_cp_for_node = total_path_cp_cost + selected_lodging_cp_cost
        return {
            "Node ID": node[config.COLUMN_NODE_ID],
            "Node Name": node[config.COLUMN_NODE_NAME],
            "Visited Nodes Info": self.format_visited_nodes(visited_node_ids, nodes_with_min_lodging_info),
            "Lodging Name": selected_lodging_name,
            "Lodging CP": selected_lodging_cp_cost,
            "Total CP": total_cp_for_node,
        }

    def find_path_and_cp(self, node_id, city_and_town_nodes, node_connection_data, nodes_with_min_lodging_info, visited_node_ids=None, total_cp_for_node=config.DEFAULT_NO_LODGING_CP_COST):
        """
        Recursively finds the cheapest path to connect a node to a city or town, calculating the total CP cost.
        
        Parameters:
            node_id (int): The ID of the current node being processed.
            city_and_town_nodes (DataFrame): DataFrame containing data for city and town nodes.
            node_connection_data (DataFrame): DataFrame detailing connections between nodes.
            nodes_with_min_lodging_info (DataFrame): Node data merged with lodging information.
            visited_node_ids (set, optional): A set of node IDs that have already been visited. Defaults to None.
            total_cp_for_node (int, optional): The accumulated CP cost for the current path. Defaults to config.DEFAULT_NO_LODGING_CP_COST.
            
        Returns:
            tuple: A tuple containing a set of visited node IDs and the total CP cost for the path.
        """
        if visited_node_ids is None:
            visited_node_ids = set()
        visited_node_ids.add(node_id)

        current_node_info = nodes_with_min_lodging_info[nodes_with_min_lodging_info[config.COLUMN_NODE_ID] == node_id].iloc[0]
        current_node_cp_cost = config.DEFAULT_NO_LODGING_CP_COST if current_node_info[config.COLUMN_CONNECTED] else current_node_info[config.COLUMN_CP_COST]
        total_cp_for_node += current_node_cp_cost

        if node_id in city_and_town_nodes[config.COLUMN_NODE_ID].values:
            return visited_node_ids, total_cp_for_node

        for connected_node in node_connection_data[node_connection_data[config.COLUMN_NODE_ID] == node_id][config.CONNECTED_NODE_ID]:
            if connected_node not in visited_node_ids:
                result_visited, result_cp = self.find_path_and_cp(
                    connected_node, city_and_town_nodes, node_connection_data, nodes_with_min_lodging_info, visited_node_ids.copy(), total_cp_for_node
                )
                if result_visited:
                    return result_visited, result_cp
        return visited_node_ids, total_cp_for_node

    def get_lodging_details(self, visited_node_ids, nodes_with_min_lodging_info):
        """
        Finds lodging details for the last city or town in the visited nodes path, which includes the lodging name and CP cost.
        
        Parameters:
            visited_node_ids (set): A set of visited node IDs during path finding.
            nodes_with_min_lodging_info (DataFrame): Node data merged with lodging information.
            
        Returns:
            tuple: A tuple containing the lodging name and its CP cost for the last visited city or town node.
        """
        for node_id in reversed(list(visited_node_ids)):
            if nodes_with_min_lodging_info.loc[nodes_with_min_lodging_info[config.COLUMN_NODE_ID] == node_id, config.COLUMN_NODE_TYPE].values[0] in config.NODE_TYPES_CITY_TOWN:
                lodging_info = nodes_with_min_lodging_info.loc[nodes_with_min_lodging_info[config.COLUMN_NODE_ID] == node_id, [config.COLUMN_LODGING_NAME, config.COLUMN_TOTAL_LODGING_CP_COST]].iloc[0]
                return lodging_info[config.COLUMN_LODGING_NAME], lodging_info[config.COLUMN_TOTAL_LODGING_CP_COST]
        return config.DEFAULT_NO_LODGING_NAME, config.DEFAULT_NO_LODGING_CP_COST

    def format_visited_nodes(self, visited_node_ids, nodes_with_min_lodging_info):
        """
        Formats the information of visited nodes for display, providing details like node name, ID, and CP cost.
        
        Parameters:
            visited_node_ids (set): A set of visited node IDs during path finding.
            nodes_with_min_lodging_info (DataFrame): Node data merged with lodging information.
            
        Returns:
            str: A string representation of the visited nodes, detailing their names, IDs, and CP costs.
        """
        formatted_visited_node_info = []
        for node_id in visited_node_ids:
            current_node_info = nodes_with_min_lodging_info.loc[nodes_with_min_lodging_info[config.COLUMN_NODE_ID] == node_id].iloc[0]
            connection_cost_text = "*0.0 CP" if current_node_info[config.COLUMN_CONNECTED] else f"{current_node_info['CP Cost']} CP"
            formatted_visited_node_info.append(f"{current_node_info['Node Name']} (ID: {node_id} - CP: {connection_cost_text})")
        return ", ".join(sorted(formatted_visited_node_info, key=lambda x: int(x.split("(ID: ")[1].split("- ")[0])))
