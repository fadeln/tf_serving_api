import base64
import json
import numpy as np
from PIL import Image
import cv2

# Load and preprocess the image
image = Image.open('paper.jpg')
image = image.resize((224, 224))  # Resize if necessary
image_array = np.array(image)

# Normalize the pixel values to the range [0, 1]
image_array = image_array / 255.0

# If your model expects a specific input shape, adjust accordingly
# For example, a common shape is (1, height, width, channels)
image_array = np.expand_dims(image_array, axis=0)

# Convert to list (or use base64 if preferred)
image_list = image_array.tolist()

# Alternatively, you can use base64 encoding
_, buffer = cv2.imencode('.jpg', (image_array[0] * 255).astype(np.uint8))
image_base64 = base64.b64encode(buffer).decode('utf-8')

# Create the payload
payload = {
    "instances": image_list  # or [{"b64": image_base64}]
}

# Save payload to a file for easy use in Postman
with open('hahahahaahah.json', 'w') as f:
    json.dump(payload, f)

print("Payload has been saved to payload.json")
