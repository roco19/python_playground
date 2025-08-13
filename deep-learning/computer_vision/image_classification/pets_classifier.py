from pathlib import Path
from fastai.learner import Learner
from fastai.vision.all import (
    ImageDataLoaders, vision_learner, untar_data, URLs, get_image_files, Resize, resnet34, error_rate
)

# Constants
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
DEFAULT_IMAGE_SIZE = 100  # Recommended size: 224. But set to 100 for performance reasons
DEFAULT_FINE_TUNING_EPOCHS = 2
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42

def is_cat(filename: str) -> str:
    """ Determine if an image filename represents a cat based on naming convention. """
    return "cat" if filename[0].isupper() else "dog"

def train_model(img_size: int = DEFAULT_IMAGE_SIZE, epochs: int = DEFAULT_FINE_TUNING_EPOCHS) -> Learner:
    """ Train a cat vs dog classifier using FastAI """
    path = untar_data(URLs.PETS) / 'images'
    dls = ImageDataLoaders.from_name_func(
        path,
        get_image_files(path),
        valid_pct=VALIDATION_SPLIT,
        seed=RANDOM_SEED,
        label_func=is_cat,
        item_tfms=Resize(img_size),
        num_workers=0 # For Windows compatibility. Should I use Conda instead?
    )

    learn = vision_learner(dls, resnet34, metrics=error_rate, pretrained=True)
    learn.fine_tune(epochs)
    return learn

def use_model(learn: Learner) -> None:
    """ Use the model to classify custom images of dogs and cats """
    test_dir = Path(__file__).parent / 'test_images'
    if test_dir.exists():
        for img_path in test_dir.glob('*'):
            if img_path.suffix.lower() in [".jpg", ".png", ".webp", ".avif"]:
                prediction, prediction_index, probs = learn.predict(img_path)
                print(f"{img_path.name}: {prediction:4} (confidence: {probs[prediction_index]:.5f})")

def main():
    print("Cat vs Dog Classifier 🐱🐶")
    print("Training model...")
    learn = train_model()

    print("\nUsing model to classify custom images.")
    use_model(learn)

    print("\nClassification complete.")

if __name__ == "__main__":
    main()
