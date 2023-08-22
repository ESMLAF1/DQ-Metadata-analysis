from flask import Flask, render_template, request
import webbrowser

app = Flask(__name__)

# Sample list of objects
object_list = ['Object 1', 'Object 2', 'Object 3', 'Object 4']

def execute_main():
    input_file_path = "data/Atradius_Metadata_Repository_for_DQ.xlsx"
    kme_definitions_file_path = "kme_definitions.yaml"
    mapping_tab_name_file = "mapping_tab_sheet_name.yaml"
    catalog_color_mapping_name_file = "mapping_catalog_style.yaml"

    # Step 1: Parse the metadata from the input Excel file.
    metadata_parser = MetadataParser(input_file_path, kme_definitions_file_path, mapping_tab_name_file)
    metadata = metadata_parser.parse_metadata()
    kme_definitions = metadata_parser.get_kme_definitions()

    # this should return a list of the AMDR elements that are not passing the validations according to KME_definitions
    # as of now the ones that are not compliant are an output in the console
    metadata_parser.validate_application_system_nodes()

    # Step 2: Create visualization object, define graph elements, build and represent lineage network
    lineage_visualizer = LineageVisualizer(metadata, catalog_color_mapping_name_file)
    nodes = lineage_visualizer.create_node_list()
    lineage_graph = lineage_visualizer.create_graph(nodes)
    lineage_visualizer.show_graph(lineage_graph)

@app.route('/')
def index():
    return render_template('index.html', object_list=object_list)

@app.route('/execute', methods=['POST'])
def execute_code():
    selected_object = request.form.get('selected_object')
    code_to_execute = request.form.get('code')
    try:
        result = eval(execute_main())
        return str(result)
    except Exception as e:
        return str(e)

if __name__ == '_main_':
    webbrowser.open('http://127.0.0.1:5000/')
    app.run(host='127.0.0.1', port='8080')