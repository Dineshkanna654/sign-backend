from PIL import Image
import os
import shutil

ARCHIVE_TEST = os.path.join("archive", "asl_alphabet_test", "asl_alphabet_test")
ARCHIVE_TRAIN = os.path.join("archive", "asl_alphabet_train", "asl_alphabet_train")
OUTPUT_DIR = "assets"
IMG_SIZE = (200, 200)


def generate_assets():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Use test images (one clean image per letter)
    for filename in os.listdir(ARCHIVE_TEST):
        if not filename.endswith(".jpg"):
            continue

        label = filename.replace("_test.jpg", "")  # e.g. "A", "space", "nothing"

        if label == "nothing":
            continue

        # Resize and save as PNG
        out_name = f"{label}.png"
        img = Image.open(os.path.join(ARCHIVE_TEST, filename))
        img = img.resize(IMG_SIZE)
        img.save(os.path.join(OUTPUT_DIR, out_name))
        print(f"Generated {out_name}")

    print(f"\nDone! Assets saved to {OUTPUT_DIR}/")


if __name__ == "__main__":
    generate_assets()
