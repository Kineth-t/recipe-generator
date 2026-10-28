import gradio as gr

def identify_ingredients(image_path):
    return "Gordon Ramsey type shit"

demo = gr.Interface(
    fn=identify_ingredients,
    inputs=gr.Image(type='filepath'),
    outputs=gr.Markdown(),
    title="Recipe Generator",
    description="Upload an image of ingredients, and the model will identify the main ingredients and suggest 3 recipes based on those ingredients.",
    flagging_mode="never"
)

demo.launch(debug=True)