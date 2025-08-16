import torch
from pathlib import Path
from fastai.learner import Learner, load_learner
from fastai.vision.all import (
    ImageDataLoaders, vision_learner, untar_data, URLs, get_image_files, Resize, resnet34, error_rate
)

# Constants
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".avif"}
DEFAULT_IMAGE_SIZE = 224  # Recommended size: 224
DEFAULT_FINE_TUNING_EPOCHS = 4
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 42
FORCE_CPU_ONLY_MODEL = False # Set to True for HuggingFace deployment
TRAINED_MODELS_PATH = Path(__file__).parent / "trained_models"
MODEL_CPU_ONLY_FILENAME = f"cpu-{Path(__file__).stem}_model.pkl"
MODEL_FILENAME = f"{Path(__file__).stem}_model.pkl"


def is_cat(filename: str) -> str:
    """ Determine if an image filename represents a cat based on naming convention. """
    return "cat" if filename[0].isupper() else "dog"

def get_model_path() -> Path:
    """ Get the path for the trained model """
    models_dir = TRAINED_MODELS_PATH
    models_dir.mkdir(exist_ok=True)
    model_name = MODEL_CPU_ONLY_FILENAME if FORCE_CPU_ONLY_MODEL else MODEL_FILENAME
    return models_dir / model_name

def train_model(img_size: int = DEFAULT_IMAGE_SIZE, epochs: int = DEFAULT_FINE_TUNING_EPOCHS) -> Learner:
    """ Train a cat vs dog classifier using FastAI """
    if FORCE_CPU_ONLY_MODEL:
        torch.cuda.is_available = lambda: False

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

def load_or_train_model(img_size: int = DEFAULT_IMAGE_SIZE, epochs: int = DEFAULT_FINE_TUNING_EPOCHS) -> Learner:
    """ Load existing model or train a new one if it doesn't exist """
    model_path = get_model_path()

    if model_path.exists():
        print(f"Loading existing model from {model_path}")
        learn = load_learner(model_path)
    else:
        print(f"Model not found at {model_path}")
        learn = train_model(img_size, epochs)

        print(f"Saving model to {model_path}")
        learn.export(model_path)

    return learn

def use_model(learn: Learner) -> None:
    """ Use the model to classify custom images of dogs and cats """
    test_dir = Path(__file__).parent / 'test_img/pets'
    if test_dir.exists():
        for img_path in test_dir.glob('*'):
            if img_path.suffix.lower() in [".jpg", ".png", ".webp", ".avif"]:
                prediction, prediction_index, probs = learn.predict(img_path)
                print(f"{img_path.name}: {prediction:4} (confidence: {probs[prediction_index]:.5f})")

def main():
    print("Cat vs Dog Classifier 🐱🐶")
    learn = load_or_train_model()

    print("\nUsing model to classify custom images.")
    use_model(learn)

    print("\nClassification complete.")

if __name__ == "__main__":
    main()
