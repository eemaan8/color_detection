from flask import Flask, request, jsonify
from color_logic import get_color_name  # Make sure this file is deployed

app = Flask(__name__)

@app.route('/')
def home():
    return "Color Detection API is running!"

@app.route('/detect_color', methods=['GET', 'POST'])
def detect_color():
    if request.method == 'POST':
        data = request.get_json()
        R = data.get('R')
        G = data.get('G')
        B = data.get('B')
    else:
        R = request.args.get('R', type=int)
        G = request.args.get('G', type=int)
        B = request.args.get('B', type=int)

    if R is None or G is None or B is None:
        return jsonify({'error': 'Missing RGB values'}), 400

    color_name = get_color_name(R, G, B)
    return jsonify({'color': color_name})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
