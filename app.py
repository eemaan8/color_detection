from flask import Flask, request, jsonify
import cv2
import numpy as np
from color_logic import get_color_name

app = Flask(__name__)

def get_average_rgb(image, center_x, center_y, size=10):
    x1 = max(center_x - size // 2, 0)
    y1 = max(center_y - size // 2, 0)
    x2 = min(center_x + size // 2, image.shape[1] - 1)
    y2 = min(center_y + size // 2, image.shape[0] - 1)

    region = image[y1:y2, x1:x2]
    avg_b = int(np.mean(region[:, :, 0]))
    avg_g = int(np.mean(region[:, :, 1]))
    avg_r = int(np.mean(region[:, :, 2]))
    return avg_r, avg_g, avg_b

@app.route('/')
def home():
    return "ClearSight Color Detection API is running!"

@app.route('/detect_color', methods=['POST'])
def detect_color():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    file_bytes = np.asarray(bytearray(file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # BGR format

    # Apply Gaussian Blur to smooth shadows/lighting
    blurred = cv2.GaussianBlur(image, (15, 15), 0)

    height, width, _ = blurred.shape
    center_y, center_x = height // 2, width // 2

    # Adaptive region size: 10% of smallest dimension (but minimum 10)
    roi_size = max(10, min(height, width) // 10)

    r, g, b = get_average_rgb(blurred, center_x, center_y, size=roi_size)

    print(f"[DEBUG] Average RGB from ROI size {roi_size}×{roi_size}: ({r}, {g}, {b})")

    color_name = get_color_name(r, g, b)

    return jsonify({
        'R': int(r),
        'G': int(g),
        'B': int(b),
        'color': color_name
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
