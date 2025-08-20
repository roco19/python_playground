from fastai.vision.all import (
    Path, DataBlock, ImageBlock, CategoryBlock, get_image_files, RegexLabeller, RandomSplitter, Resize, Learner,
    resnet34, vision_learner, error_rate
)

# Constants
DEFAULT_IMAGE_SIZE = 100  # Recommended size: 224. But set to 100 for performance reasons
DEFAULT_FINE_TUNING_EPOCHS = 15
VALIDATION_SPLIT = 0.2
RANDOM_SEED = 20
REGEX_HOUSE_LABEL = r"^([^-]+)" # Extracts 'colonial' or 'victorian' from filename
TRAINING_SET_PATH = "training_img/houses"


def train_model(img_size: int = DEFAULT_IMAGE_SIZE, epochs: int = DEFAULT_FINE_TUNING_EPOCHS) -> Learner:
    """ Train a House classifier using FastAI """
    path = Path(TRAINING_SET_PATH)

    data_block = DataBlock(
        blocks=[ImageBlock, CategoryBlock],
        get_items=get_image_files,
        splitter=RandomSplitter(valid_pct=VALIDATION_SPLIT, seed=RANDOM_SEED),
        get_y=RegexLabeller(pat=REGEX_HOUSE_LABEL),
        item_tfms=[Resize(img_size, method="squish")]
    )

    data_loaders = data_block.dataloaders(path, bs=4, num_workers=0) # "num_workers=0" For Windows compatibility.
    print(f"Train batches: {len(data_loaders.train)}")
    print(f"Valid batches: {len(data_loaders.valid)}")

    # Uncomment this snippet to see the batch
    # data_loaders.show_batch(max_n=5)
    # pyplot.show()

    learn = vision_learner(data_loaders, resnet34, metrics=error_rate, pretrained=True)
    learn.fine_tune(epochs)
    return learn

def use_model(learn: Learner) -> None:
    """ Use the model to classify custom images """
    test_dir = Path(__file__).parent / 'test_img/houses'
    if test_dir.exists():
        for img_path in test_dir.glob('*'):
            if img_path.suffix.lower() in [".jpg", ".png", ".webp", ".avif"]:
                prediction, prediction_index, probs = learn.predict(img_path)
                print(f"{img_path.name}: {prediction:4} (confidence: {probs[prediction_index]:.5f})")

def main():
    print("House Classifier 🏠")
    print("Training model...")
    learn = train_model()

    print("\nUsing model to classify custom images.")
    use_model(learn)

    print("\nClassification complete.")


if __name__ == "__main__":
    main()