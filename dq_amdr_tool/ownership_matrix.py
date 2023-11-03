import duckdb
from pandas import DataFrame


class OwnershipMatrix:
    def __init__(self, metadata):
        self.metadata = metadata
        self.matrix_df = None

    def create_matrix(self):
        # Implement logic to create the ownership matrix table based on the metadata.
        # The table should show the steward and data owner for each table.
        # You can use pandas DataFrame or any other suitable data structure.
        #asset_status as status,
        self.query = "select distinct subtitle as 'System - DataSource', data_owner as 'Data Source Owner', data_Steward as 'Data Steward', Data_Usage_Owner as 'Data Usage Owner', Data_Custodian as 'Data Custodian', Data_Consumers as 'SME' from tables where data_owner is not null order by subtitle ASC"
        self.matrix_df = duckdb.query(self.query).df()

    def save_matrix_to_html(self, output_path):
        # Save the ownership matrix table to an HTML file in the specified output_path.
        if self.matrix_df is not None:
            self.matrix_df.to_html(output_path, index=False)
            header1 = "<h1>IFRS17 Matrix Ownership</h1>"
            linkemail = '<p>For any questions or corrections about the matrix, please contact <a href="mailto:EnterpriseDataManagement@atradius.com?subject=[Matrix Ownership]">EnterpriseDataManagement@atradius.com</a></p>'
            f = open(output_path, 'r+')
            lines = f.readlines()
            f.seek(0)
            f.write(header1 + '\n')
            f.write(linkemail + '\n')
            f.write('<style>' + '\n')
            f.write('th, td {text-align: left;}' + '\n')
            f.write('thead {background-color: #FFAA99;}' + '\n')
            f.write('tr:hover {background-color: #FFAA99;}' + '\n')
            f.write('</style>' + '\n')
            for line in lines:
                f.write(line.replace("None", "").replace("none", ""))
            f.close