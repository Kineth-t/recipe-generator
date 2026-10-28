import base64
import mimetypes
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

image_path = "images/ingredients.png"

with open(image_path, "rb") as f:
    raw_binary = f.read()
    base64_bytes = base64.b64encode(raw_binary)
    image_base64 = base64_bytes.decode("utf-8")
    mime_type = mimetypes.guess_type(image_path)[0]

# Initialise the model
model = init_chat_model("gemini-3.6-flash", model_provider="google_genai")

# System prompt
system_prompt =  """
"You are a helpful chef. Identify the main ingredients. Suggest 3 recipe based on those ingredients.
"""

# Create message
message = [{"role": "system", "content": system_prompt},
           {"role": "user", 
           "content": [
               {"type": "image", "base64": image_base64, "mime_type": mime_type}
            ]
        }]

# Get and print the response
response = model.invoke(message)
print(response.text)