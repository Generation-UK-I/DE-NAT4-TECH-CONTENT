import requests
from PIL import Image
from io import BytesIO

# 1. Define the API endpoint
url = "https://cataas.com/cat"

# 2. Make a GET request to the API
response = requests.get(url)

# 3. Check the request was successful
print(f"Status code: {response.status_code}")

# 4. Load the image from the response and display it
image = Image.open(BytesIO(response.content))
image.show()