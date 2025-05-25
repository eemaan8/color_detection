from flask import Flask, request, jsonify
from color_logic import get_color_name  # Import shared logic

app = Flask(__name__)

@app.route('/detect_color', methods=['GET', 'POST'])
def detect_color():
    if request.method == 'POST':
        data = request.get_json()
        R = data.get('R')
        G = data.get('G')
        B = data.get('B')
    else:  # GET method
        R = request.args.get('R', type=int)
        G = request.args.get('G', type=int)
        B = request.args.get('B', type=int)

    if R is None or G is None or B is None:
        return jsonify({'error': 'Missing RGB values'}), 400

    color_name = get_color_name(R, G, B)
    return jsonify({'color': color_name})

if __name__ == '__main__':
    app.run(debug=True)
