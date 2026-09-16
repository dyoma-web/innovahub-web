"""Recupera los íconos 3D oficiales del brochure (JPEG color + PNG máscara → PNG RGBA).

Uso: python tools/brochure_assets.py
Lee ../Brochure-IH-fundaciones.pdf y escribe assets/img/marca/*.png
"""
import io
from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT.parent / "Brochure-IH-fundaciones.pdf"
OUT = ROOT / "assets" / "img" / "marca"
OUT.mkdir(parents=True, exist_ok=True)

# página (1-based), nombre de salida, tamaño mínimo (ancho) para identificar la pareja color+máscara
WANTED = {
    2: ("esfera-3d", 380),
    3: ("escena-hub-3d", 300),
    8: ("globo-3d", 600),
    9: ("isologo-3d", 350),
    10: ("icono-formacion", 280),
    11: ("icono-diagnostico", 190),
    12: ("icono-sistematizacion", 280),
    13: ("icono-produccion", 280),
    20: ("icono-plataformas", 280),
}

doc = fitz.open(PDF)
for pno, (name, minw) in WANTED.items():
    page = doc[pno - 1]
    color, mask = None, None
    for img in page.get_images(full=True):
        info = doc.extract_image(img[0])
        w, h = info["width"], info["height"]
        if w < minw:
            continue
        im = Image.open(io.BytesIO(info["image"]))
        if info["ext"] in ("jpeg", "jpg") and color is None:
            color = im.convert("RGB")
        elif info["ext"] == "png" and mask is None:
            mask = im.convert("L")
        if color is not None and mask is not None and color.size == mask.size:
            break
    if color is None:
        print("sin color:", name)
        continue
    if mask is not None and mask.size == color.size:
        rgba = color.copy()
        rgba.putalpha(mask)
    else:
        # Sin máscara: hacer transparente el blanco puro
        rgba = color.convert("RGBA")
        px = rgba.load()
        for y in range(rgba.height):
            for x in range(rgba.width):
                r, g, b, a = px[x, y]
                if r > 246 and g > 246 and b > 246:
                    px[x, y] = (r, g, b, 0)
    # recorte al contenido
    bbox = rgba.getchannel("A").getbbox()
    if bbox:
        rgba = rgba.crop(bbox)
    rgba.save(OUT / f"{name}.png", optimize=True)
    print(name, rgba.size)
