import torch
import clip
from PIL import Image
from dotenv import load_dotenv
from pprint import pprint
import math
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Initialize device and load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# List of items to detect in images
item_prompts = [
    "chicken", "salmon", "shrimp", "egg",
    "carrot", "broccoli", "spinach", "tomato", "potato",
    "apple", "banana", "orange", "grape", "strawberry",
    "milk", "cheese", "yogurt", "bread", "chocolate",
    "lettuce", "onion", "garlic", "butter",
    "lemon", "pomegranate", "green beans", "cauliflower", "bell pepper",
    "eggplant", "baguette", "ginger", "pasta", "radish",
    "parsley", "artichoke", "cabbage", "red beans"
]

# Encode text prompts as reference embeddings
with torch.no_grad():
    text_inputs = model.encode_text(torch.cat([clip.tokenize(f"a photo of a {item}") for item in item_prompts]).to(device))

def one_week_from_now():
    """Returns the date and time exactly one week from now."""
    return datetime.now() + timedelta(weeks=1)

class FridgyClipper:
    def __init__(self, patch_size=224, stride=112, threshold=0.8, batch_size=16, nms_threshold=0.5):
        self.patch_size = patch_size
        self.stride = stride
        self.threshold = threshold
        self.batch_size = batch_size
        self.nms_threshold = nms_threshold

    def identify_grocery_items(self, image):
        """
        Detects items in an image and returns an inventory prompt with item counts.
        """
        width, height = image.size
        item_counts = {}
        patches, positions = [], []

        # Slide a window to create patches
        for top in range(0, height - self.patch_size + 1, self.stride):
            for left in range(0, width - self.patch_size + 1, self.stride):
                patch = image.crop((left, top, left + self.patch_size, top + self.patch_size))
                patches.append(preprocess(patch).unsqueeze(0).to(device))
                positions.append((left, top, left + self.patch_size, top + self.patch_size))

                # Process patches in batches
                if len(patches) == self.batch_size:
                    self._process_batch(patches, positions, item_counts)
                    patches, positions = [], []

        # Process any remaining patches
        if patches:
            self._process_batch(patches, positions, item_counts)

        # Apply ceiling to counts
        item_counts = {item: math.ceil(count) for item, count in item_counts.items()}

        # Create an inventory prompt
        item_list = [f"{item}: {count}" for item, count in item_counts.items()]
        prompt = f"Add these items to my inventory:\n\nItems:\n" + "\n".join(item_list) + f"\n\nExpiry: {one_week_from_now()}" + "\n\n"
        
        # Print item counts
        print("Item Counts:")
        pprint(item_counts)
        return prompt

    def _process_batch(self, patches, positions, item_counts, item_increment=0.33):
        """
        Processes a batch of patches, identifies items, and updates item counts.
        """
        batch = torch.cat(patches).to(device)
        with torch.no_grad():
            image_features = model.encode_image(batch)
            similarity = (100.0 * image_features @ text_inputs.T).softmax(dim=-1)
            values, indices = similarity.topk(1, dim=-1)

        detected_positions = []
        for i in range(len(patches)):
            if values[i, 0].item() > self.threshold:
                item_name = item_prompts[indices[i, 0].item()]
                position = positions[i]

                # Apply NMS to avoid duplicate detections
                if not self._is_duplicate(item_name, position, detected_positions):
                    detected_positions.append((item_name, position))
                    item_counts[item_name] = item_counts.get(item_name, 0) + item_increment

    def _is_duplicate(self, item_name, position, detected_positions):
        """
        Checks if a detected item overlaps significantly with previous detections.
        """
        for detected_item, detected_pos in detected_positions:
            if detected_item == item_name and self._calculate_overlap(position, detected_pos) > self.nms_threshold:
                return True
        return False

    def _calculate_overlap(self, boxA, boxB):
        """
        Calculates Intersection over Union (IoU) between two boxes to measure overlap.
        """
        xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
        xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])
        inter_area = max(0, xB - xA) * max(0, yB - yA)
        boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return inter_area / float(boxA_area + boxB_area - inter_area)
