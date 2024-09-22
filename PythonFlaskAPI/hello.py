from flask import jsonify
from PythonFlaskAPI import app

@app.route('/data', methods=['GET'])
def data():
    return jsonify(
        {'message': 'Hello World!'}
    )
    
