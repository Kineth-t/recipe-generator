import gradio as gr
import base64
import mimetypes
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Output schema - the structure the model must return
# A single recipe
class Recipe(BaseModel):
    name: str
    description: str = Field(description="One-sentence summary of the dish")
    cook_time: str = Field(description="e.g. '25 mins'")
    ingredients: list[str]
    steps: list[str] = Field(description="Short, concise cooking steps")

# The full response: detected ingredients + recipe suggestions
class RecipeResponse(BaseModel):
    main_ingredients: list[str]
    recipes: list[Recipe] = Field(description="Exactly 3 recipes")

# Initialise model
model = init_chat_model("gemini-3.6-flash", model_provider="google_genai")
# Wrap the model so it returns a RecipeResponse object instead of free text
structured_model = model.with_structured_output(RecipeResponse)

# System prompt
system_prompt = """
You are a helpful chef. Identify the main ingredients in the image. Suggest 3 recipes based on those ingredients.
Keep each recipe concise: no more than 8 steps, one sentence per step.
"""

# Convert a Recipe object into Markdown for display
def format_recipe(recipe):
    # Bulleted ingredient list and numbered steps
    ingredients = "\n".join(f"- {i}" for i in recipe.ingredients)
    steps = "\n".join(f"{n}. {s}" for n, s in enumerate(recipe.steps, 1))
    return f"""### {recipe.name}
*{recipe.description}*

⏱️ **Cook time:** {recipe.cook_time}

**Ingredients**
{ingredients}

**Steps**
{steps}
"""

# Main function - runs when the button is clicked
def identify_ingredients(image_path):
    # Read the image and encode it as base64 to send to the model
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
        response = structured_model.invoke(message)

    # Format the outputs for display
    ingredients = "**Main ingredients:** " + ", ".join(response.main_ingredients)
    # Keep at most 3 recipes
    recipes = [format_recipe(r) for r in response.recipes[:3]]
    # Pad with empty strings if fewer than 3, so there is always one value per tab
    recipes += [""] * (3 - len(recipes))
    # Returns 4 values, matching the 4 outputs in submit.click below
    return ingredients, *recipes

# UI layout
with gr.Blocks(title="Recipe Generator") as demo:
    gr.Markdown("# Recipe Generator\nUpload an image of ingredients, and the model will identify the main ingredients and suggest 3 recipes based on those ingredients.")
    # Split the page into left and right columns
    with gr.Row():
        # Left: image upload and button
        with gr.Column(scale=1):
            image = gr.Image(type="filepath")
            submit = gr.Button("Generate recipes", variant="primary")
        # Right: ingredients summary and one tab per recipe
        with gr.Column(scale=1):
            ingredients_out = gr.Markdown()
            with gr.Tabs():
                recipe_outs = []
                for n in range(1, 4):
                    with gr.Tab(f"Recipe {n}"):
                        # max_height makes long recipes scroll instead of stretching the page
                        recipe_outs.append(gr.Markdown(max_height=500))

    # When the button is clicked, pass the image to identify_ingredients
    # and send its 4 return values to the 4 output boxes, in order
    submit.click(identify_ingredients, inputs=image, outputs=[ingredients_out, *recipe_outs])

# Start the local web server
demo.launch(debug=True)
