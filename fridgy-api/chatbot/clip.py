import torch
import clip
from PIL import Image
from dotenv import load_dotenv
from pprint import pprint
import math
from datetime import datetime, timedelta

# Load environment variables (if any)
load_dotenv()

# Initialize device and load the CLIP model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# List of items to detect in images (halal/kosher)
item_prompts = [
    "chicken", "meat", "lamb", "turkey", "goat", "duck", "quail", "fish", "shrimp", 
    "salmon", "trout", "tuna", "bass", "cod", "haddock", "tilapia", "mackerel",
    "carrot", "broccoli", "spinach", "kale", "lettuce", "cabbage", "onion", "garlic", 
    "tomato", "pepper", "potato", "eggplant", "zucchini", "cucumber", "celery", 
    "cauliflower", "peas", "beans", "corn", "beet", "radish", "squash", "turnip", 
    "mushroom", "okra", "leek", "parsley", "cilantro", "chard", "asparagus",
    "apple", "banana", "grape", "orange", "lemon", "lime", "pear", "peach", "plum", 
    "mango", "melon", "berry", "cherry", "kiwi", "fig", "date", "apricot", "guava", 
    "papaya", "pineapple", "grapefruit", "pomegranate", "tangerine", "nectarine",
    "milk", "cheese", "yogurt", "cream", "butter", "eggs", "buttermilk", "whey",
    "chocolate", "flour", "sugar", "salt", "yeast", "bread", "soda", "vinegar",
    "vanilla", "cocoa", "honey", "maple", "syrup", "oil", "mushroom"
]

# Encode text prompts for each item to use as reference embeddings
with torch.no_grad():
    text_inputs = model.encode_text(torch.cat([clip.tokenize(f"a photo of a {item}") for item in item_prompts]).to(device))

def one_week_from_now():
    # Get the current date and time and 
    # Calculate 1 week from now
    return datetime.now() + timedelta(weeks=1)
class FridgyClipper:
    def __init__(self, patch_size=224, stride=112, threshold=0.8, batch_size=16, nms_threshold=0.5):
        self.patch_size = patch_size      # Size of each patch for detection
        self.stride = stride              # Stride between patches
        self.threshold = threshold        # Confidence threshold for detection
        self.batch_size = batch_size      # Number of patches processed in each batch
        self.nms_threshold = nms_threshold  # Threshold for non-maximum suppression (NMS)

    def identify_grocery_items(self, image):
        """
        Detects items in an image and returns an inventory prompt with item counts.
        """
        width, height = image.size
        item_counts = {}  # Dictionary to store detected item counts
        patches, positions = [], []

        # Slide a window across the image to create patches
        for top in range(0, height - self.patch_size + 1, self.stride):
            for left in range(0, width - self.patch_size + 1, self.stride):
                # Crop patch from the image and preprocess it
                patch = image.crop((left, top, left + self.patch_size, top + self.patch_size))
                patches.append(preprocess(patch).unsqueeze(0).to(device))
                positions.append((left, top, left + self.patch_size, top + self.patch_size))

                # Process patches in batches for efficiency
                if len(patches) == self.batch_size:
                    self._process_batch(patches, positions, item_counts)
                    patches, positions = [], []

        # Process any remaining patches
        if patches:
            self._process_batch(patches, positions, item_counts)

        # Apply ceiling to counts to ensure whole numbers
        item_counts = {item: math.ceil(count) for item, count in item_counts.items()}

        # Create a prompt listing detected items and counts
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
            # Encode image patches and calculate similarity with item text embeddings
            image_features = model.encode_image(batch)
            similarity = (100.0 * image_features @ text_inputs.T).softmax(dim=-1)
            values, indices = similarity.topk(1, dim=-1)

        detected_positions = []
        for i in range(len(patches)):
            # If confidence is above threshold, consider the detection
            if values[i, 0].item() > self.threshold:
                item_name = item_prompts[indices[i, 0].item()]
                position = positions[i]

                # Apply NMS to avoid counting overlapping items multiple times
                if not self._is_duplicate(item_name, position, detected_positions):
                    detected_positions.append((item_name, position))
                    # Increment count by a fraction to account for overlap
                    item_counts[item_name] = item_counts.get(item_name, 0) + item_increment

    def _is_duplicate(self, item_name, position, detected_positions):
        """
        Checks if a detected item overlaps significantly with previous detections (NMS).
        """
        for detected_item, detected_pos in detected_positions:
            # If the same item and significant overlap, treat as duplicate
            if detected_item == item_name and self._calculate_overlap(position, detected_pos) > self.nms_threshold:
                return True
        return False

    def _calculate_overlap(self, boxA, boxB):
        """
        Calculates Intersection over Union (IoU) between two boxes to measure overlap.

        Parameters:
        - boxA, boxB: Bounding boxes in (x1, y1, x2, y2) format.

        Returns:
        - IoU (ratio) of overlap between 0 (no overlap) and 1 (full overlap).
        """
        # Find intersection rectangle coordinates
        xA, yA = max(boxA[0], boxB[0]), max(boxA[1], boxB[1])
        xB, yB = min(boxA[2], boxB[2]), min(boxA[3], boxB[3])

        # Calculate intersection area (0 if no overlap)
        inter_area = max(0, xB - xA) * max(0, yB - yA)

        # Calculate areas of each box
        boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])

        # Calculate IoU: intersection area divided by combined area
        return inter_area / float(boxA_area + boxB_area - inter_area)
