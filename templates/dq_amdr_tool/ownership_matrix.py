import pandas as pd


class OwnershipMatrix:
    def __init__(self, metadata):
        self.metadata = metadata
        self.matrix_df = None

    # def create_matrix(self):
    # Implement logic to create the ownership matrix table based on the metadata.
    # The table should show the steward and data owner for each table.
    # You can use pandas DataFrame or any other suitable data structure.

    # Example:
    # matrix_data = {
    #    'Table': [],
    #    'Steward': [],
    #    'Data Owner': []
    # }
    # for table_info in self.metadata['Tables']:
    #    matrix_data['Table'].append(table_info['name'])
    #    matrix_data['Steward'].append(table_info.get('steward', 'N/A'))
    #    matrix_data['Data Owner'].append(table_info.get('data_owner', 'N/A'))
    #
    # self.matrix_df = pd.DataFrame(matrix_data)

    def save_matrix_to_html(self, output_path):
        # Save the ownership matrix table to an HTML file in the specified output_path.
        if self.matrix_df is not None:
            self.matrix_df.to_html(output_path, index=False)
