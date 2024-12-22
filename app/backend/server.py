import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import pandas as pd
from backend.operations import OperationsHandler
from backend.database import DatabaseHandler
from flask_cors import CORS

class AppServer:
    def __init__(self):
        self.app = Flask(__name__, static_folder='frontend/templates')
        self.app.config['UPLOAD_FOLDER'] = 'uploads'

        # Set the api key
        self.api_key = "Replace this with your API key"
        os.makedirs(self.app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Initialize handlers
        self.db_handler = DatabaseHandler()
        self.operations_handler = OperationsHandler(self.api_key)

        # Initialize routes
        self._init_routes()

        # Enable CORS
        CORS(self.app)

    def _init_routes(self):
        @self.app.route('/upload', methods=['POST'])
        def upload_file():
            try:
                if 'file' not in request.files:
                    return jsonify({"error": "No file uploaded"}), 400
                file = request.files['file']
                if file.filename == '':
                    return jsonify({"error": "No file selected"}), 400
                if file and (file.filename.endswith('.xlsx') or file.filename.endswith('.csv')):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)

                    # Extract numerical columns
                    df = pd.read_excel(file_path) if filename.endswith('.xlsx') else pd.read_csv(file_path)
                    numerical_columns = df.select_dtypes(include=['float64', 'int64']).to_dict(orient='list')

                    return jsonify({"columns": numerical_columns}), 200
                return jsonify({"error": "Invalid file format"}), 400
            except Exception as e:
                return jsonify({"error": f"File upload failed: {str(e)}"}), 500

        @self.app.route('/process', methods=['POST'])
        def process_data():
            try:
                data = request.json
                column = data.get('column')
                operation = data.get('operation')
                if not column or not operation:
                    return jsonify({"error": "Invalid request data"}), 400

                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], 'test.csv')
                if not os.path.exists(file_path):
                    return jsonify({"error": "Uploaded file not found"}), 404

                df = pd.read_csv(file_path)
                if column not in df:
                    return jsonify({"error": f"Column {column} not found in file"}), 400
                values = df[column].tolist()
                result = self.operations_handler.process_operation(column, operation, values)
                session_id = request.remote_addr
                try:
                    self.db_handler.save_result(session_id, column, operation, result)
                except Exception as e:
                    print("Could not save result")

                return jsonify({"result": result}), 200
            except Exception as e:
                return jsonify({"error": f"Processing failed: {str(e)}"}), 500

        @self.app.route('/results', methods=['GET'])
        def get_results():
            try:
                session_id = request.remote_addr
                results = self.db_handler.fetch_results(session_id)
                return jsonify(results), 200
            except Exception as e:
                return jsonify({"error": f"Failed to fetch results: {str(e)}"}), 500

    def run(self, host='0.0.0.0', port=5001):
        self.app.run(host=host, port=port)


if __name__ == '__main__':
    server = AppServer()
    server.run()
