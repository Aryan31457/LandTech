from flask import Flask, request, jsonify
from io import BytesIO
import requests
from flask_cors import CORS
from PIL import Image
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

app = Flask(__name__)
CORS(app)
# Configure Cloudinary
CLOUDINARY_URL = "https://api.cloudinary.com/v1_1/dq1zewmkm/image/upload"
CLOUDINARY_UPLOAD_PRESET = "ml_default"

import cv2
import numpy as np

def post_process_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

    # Perform morphological operations
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    # Convert back to RGB
    processed_img = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
    cv2.imwrite('processed_image.png', processed_img)

    return processed_img

def execute_notebook_and_get_function_output(prompt):
    # Load the notebook
    with open("model.ipynb") as f:
        notebook = nbformat.read(f, as_version=4)

    # Execute the notebook
    ep = ExecutePreprocessor(timeout=300, kernel_name="python3")
    ep.preprocess(notebook)

    # Extract and execute the function
    global_namespace = {}
    exec("\n".join([cell["source"] for cell in notebook.cells if cell["cell_type"] == "code"]), global_namespace)

    # Call the function defined in the notebook
    return global_namespace["generate_image_from_text"](prompt)

# Upload image to Cloudinary
def upload_to_cloudinary(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    files = {"file": buffer}
    data = {"upload_preset": CLOUDINARY_UPLOAD_PRESET}

    response = requests.post(CLOUDINARY_URL, files=files, data=data)
    # print(response)
    response_data = response.json()
    # print(response_data)
    return response_data["secure_url"]

@app.route('/generate-map', methods=['POST'])
def generate_map():
    try:
        # Get prompt from the frontend
        data = request.json
        prompt = data.get("prompt")
        print(prompt)
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate floor map using the model
        generated_image = execute_notebook_and_get_function_output(prompt)
        # generated_image = post_process_image("./generated_image.png")

        # Upload to Cloudinary
        cloudinary_url = upload_to_cloudinary(generated_image)

        # Return the Cloudinary URL
        return jsonify({"image_url": cloudinary_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
