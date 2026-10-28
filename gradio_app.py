import gradio as gr
import base64
import mimetypes
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialise model
model = init_chat_model("gemini-3.6-flash", model_provider="google_genai")

# System prompt
system_prompt =  """
"You are a helpful chef. Identify the main ingredients. Suggest 3 recipe based on those ingredients.
"""

# 
def identify_ingredients(image_path):
    with open(image_path, "rb") as f:
        raw_binary = f.read()
        base64_bytes = base64.b64encode(raw_binary)
        image_base64 = base64_bytes.decode("utf-8")
        mime_type = mimetypes.guess_type(image_path)[0]

        # Create message
        message = [{"role": "system", "content": system_prompt},
           {"role": "user", 
           "content": [
               {"type": "image", "base64": image_base64, "mime_type": mime_type}
            ]
        }]

        # Response from model
        response = model.invoke(message)
    return response.text

demo = gr.Interface(
    fn=identify_ingredients,
    inputs=gr.Image(type='filepath'),
    outputs=gr.Markdown(),
    title="Recipe Generator",
    description="Upload an image of ingredients, and the model will identify the main ingredients and suggest 3 recipes based on those ingredients.",
    flagging_mode="never"
)

demo.launch(debug=True)