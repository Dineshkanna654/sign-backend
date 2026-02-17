from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from PIL import Image
import base64
import os
import io

app = FastAPI(title="ASL Sign Language API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ASSETS_DIR = "assets"

# Serve letter images directly at /assets/A.png etc.
if os.path.exists(ASSETS_DIR):
    app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")


class TextPayload(BaseModel):
    text: str


@app.get("/")
def read_root():
    return {"status": "ok", "endpoints": ["/api/text-to-sign", "/api/letters/{letter}"]}


@app.get("/api/letters/{letter}")
async def get_letter(letter: str):
    """Get a single ASL letter image."""
    letter = letter.upper()
    if letter == " ":
        letter = "space"

    img_path = os.path.join(ASSETS_DIR, f"{letter}.png")
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail=f"No sign for '{letter}'")

    return StreamingResponse(open(img_path, "rb"), media_type="image/png")


@app.post("/api/text-to-sign")
async def text_to_sign(payload: TextPayload):
    """Convert text to ASL sign language. Returns per-letter base64 images + a combined image."""
    text = payload.text.upper()

    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    letters = []
    images = []

    for char in text:
        if char == " ":
            label = "space"
        elif char.isalpha():
            label = char
        else:
            continue

        img_path = os.path.join(ASSETS_DIR, f"{label}.png")
        if not os.path.exists(img_path):
            continue

        img = Image.open(img_path)
        images.append(img)

        # Base64 encode each letter
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()

        letters.append({
            "char": char,
            "label": label,
            "image": f"data:image/png;base64,{b64}",
        })

    if not images:
        raise HTTPException(status_code=400, detail="No valid characters found.")

    # Combined horizontal strip
    widths, heights = zip(*(i.size for i in images))
    combined = Image.new("RGB", (sum(widths), max(heights)), (255, 255, 255))
    x = 0
    for im in images:
        combined.paste(im, (x, 0))
        x += im.size[0]

    buf = io.BytesIO()
    combined.save(buf, format="PNG")
    combined_b64 = base64.b64encode(buf.getvalue()).decode()

    return {
        "text": payload.text,
        "letters": letters,
        "combined_image": f"data:image/png;base64,{combined_b64}",
    }
