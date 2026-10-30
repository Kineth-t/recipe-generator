# Recipe Generator

Upload a photo of your ingredients. The app identifies the main ingredients and suggests 3 recipes you can make with them.

I built this as a side project to learn how to work with LLMs, agents and image input. Feel free to try it out, and swap in whatever model you like.

## How it works

The image is sent to a vision-capable chat model through [LangChain](https://python.langchain.com/). The model returns structured output (Pydantic models), so you get a list of ingredients plus 3 recipes, each with a name, description, cook time, ingredients and steps. [Gradio](https://www.gradio.app/) displays the result in a web page with one tab per recipe.

## Project structure

| File | Description |
|---|---|
| `gradio_app.py` | Web app: upload an image, get recipes in tabs |
| `generate_recipe.py` | Command-line version: reads `images/ingredients.png` and prints the response |
| `images/` | Sample ingredient image |
| `.env.example` | Template for your API keys |
| `requirements.txt` | Pinned dependencies |

## Setup

Requires Python 3.13.

```bash
git clone https://github.com/Kineth-t/recipe-generator.git
cd recipe-generator

python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
```

Then open `.env` and add your API key. The default model is Google Gemini, so you need a `GOOGLE_API_KEY` ([get one here](https://aistudio.google.com/apikey)).

## Usage

**Web app**

```bash
python gradio_app.py
```

Open the local URL printed in the terminal (usually http://127.0.0.1:7860), upload an image and click **Generate recipes**.

**Command line**

```bash
python generate_recipe.py
```

To use a different photo, change `image_path` in `generate_recipe.py`.

## Changing the model

The model is set in one line in each script:

```python
model = init_chat_model("gemini-3.6-flash", model_provider="google_genai")
```

To use OpenAI instead (`langchain-openai` is already installed):

1. Set `OPENAI_API_KEY` in `.env`.
2. Change the line to:
   ```python
   model = init_chat_model("<openai-model-name>", model_provider="openai")
   ```

Any provider supported by LangChain's [`init_chat_model`](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html) works too, as long as you install its package (for example `langchain-anthropic`) and set its API key.

Whichever model you pick must:
- accept **image input**, and
- support **structured output**, which `gradio_app.py` needs.
