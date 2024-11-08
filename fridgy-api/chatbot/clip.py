from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import torch
from torchvision import transforms
import clip
import os
from dotenv import load_dotenv

# Load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Define possible grocery items (classes) to identify
item_prompts = [
    "Green Apples",
    "Bananas",
    "Baguette",
    "Lettuce",
    "Ginger",
    "Oranges",
    "Tomatoes",
    "Milk Bottle",
    "Artichoke",
    "Pomegranate",
    "Cauliflower",
    "Eggs",
    "Carrots",
    "Leeks",
    "Potatoes",
    "Mushrooms",
    "Eggplant",
    "Red Bell Pepper",
    "Radishes",
    "Cilantro",
    "Romaine Lettuce",
    "Green Beans",
    "Dry Spaghetti Pasta",
    "Red Kidney Beans"
]
text_inputs = torch.cat([clip.tokenize(f"a photo of a {item}") for item in item_prompts]).to(device)

from chatbot.prompts import MAIN_PROMPT 

class FridgyClipper:

    def __init__(self):
        self.context = [{'role': 'system', 'content': MAIN_PROMPT}]
    
    def identify_grocery_items(self, image):
        # Preprocess the image for CLIP
        preprocess_image = preprocess(image).unsqueeze(0).to(device)

        # Compute similarity between image and text labels
        with torch.no_grad():
            image_features = model.encode_image(preprocess_image)
            text_features = model.encode_text(text_inputs)
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            values, indices = similarity[0].topk(len(item_prompts))  # Get top 5 matches

        # Get detected items
        detected_items = [item_prompts[i] for i in indices]

        augmented_prompt = f"Count the items and add to my inventory\n Items : {', '.join(detected_items)}"
        return augmented_prompt


