from flask import Flask, request, jsonify
from color_logic import get_color_name
import cv2
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

@app.route('/')
def home():
    return "Color Detection API is running!"

@app.route('/detect_color', methods=['POST'])
def detect_color():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']

    # Read image as numpy array
    image = Image.open(image_file.stream).convert('RGB')
    image_np = np.array(image)

    # Get center pixel
    height, width, _ = image_np.shape
    center_y, center_x = height // 2, width // 2
    R, G, B = image_np[center_y, center_x]

    # Get color name from CSV
    color_name = get_color_name(R, G, B)

    return jsonify({
        'R': int(R),
        'G': int(G),
        'B': int(B),
        'color': color_name
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
