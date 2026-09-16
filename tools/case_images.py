"""Compone las imágenes 16:10 de los casos (1200x750) a partir de capturas de los
productos publicados y de las portadas/fotogramas recuperados del brochure.

Uso: python tools/case_images.py
Salida: assets/img/casos/*.jpg
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
CAP = ROOT.parent / "_fuentes" / "capturas"
BRO = ROOT.parent / "_fuentes" / "brochure"
OUT = ROOT / "assets" / "img" / "casos"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1200, 750
PAL = {"coral": "#DA5A49", "naranja": "#DD7A3E", "ocre": "#EAC44C", "keppel": "#45AD98",
       "charcoal": "#334D5C", "blue": "#363F4E", "deep": "#1E2F3D"}


def cover(src, top=0.0):
    """Recorta una captura al formato 16:10 (anclado arriba)."""
    im = Image.open(src).convert("RGB")
    r = W / im.width
    im = im.resize((W, round(im.height * r)), Image.LANCZOS)
    y0 = min(max(0, round(top * (im.height - H))), max(0, im.height - H))
    return im.crop((0, y0, W, y0 + H))


def iso_pattern(base, accent):
    """Fondo de marca con retícula isométrica sutil."""
    bg = Image.new("RGB", (W, H), base)
    d = ImageDraw.Draw(bg, "RGBA")
    step = 48
    for x in range(-H, W + H, step):
        d.line([(x, 0), (x + H * 0.577, H)], fill=(255, 255, 255, 14), width=1)
        d.line([(x, 0), (x - H * 0.577, H)], fill=(255, 255, 255, 14), width=1)
    # bloque de color de la línea en la esquina
    d.rectangle([(0, H - 14), (W, H)], fill=accent)
    d.rectangle([(W - 160, 0), (W, 14)], fill=accent)
    return bg


def rounded_shadow(img, radius=18, blur=28, offset=24, alpha=110):
    """Devuelve (capa RGBA con sombra, máscara redondeada)."""
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (img.width - 1, img.height - 1)], radius=radius, fill=255)
    pad = blur * 2
    shadow = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    sm = Image.new("L", shadow.size, 0)
    ImageDraw.Draw(sm).rounded_rectangle([(pad, pad + offset), (pad + img.width, pad + img.height + offset)], radius=radius, fill=alpha)
    sm = sm.filter(ImageFilter.GaussianBlur(blur))
    shadow.putalpha(sm)
    return shadow, mask, pad


def framed(src, base, accent, width=0.74, mockup=None):
    """Imagen pequeña presentada sobre fondo de marca con sombra (portadas, fotogramas)."""
    bg = iso_pattern(base, accent).convert("RGBA")
    im = Image.open(src).convert("RGB")
    if mockup == "video":
        # barra de reproductor debajo del fotograma
        tw = round(W * width)
        th = round(im.height * tw / im.width)
        im = im.resize((tw, th), Image.LANCZOS)
        bar = Image.new("RGB", (tw, 44), "#141C24")
        bd = ImageDraw.Draw(bar)
        bd.polygon([(20, 12), (20, 32), (38, 22)], fill="#FFFFFF")
        bd.rectangle([(56, 20), (tw - 24, 24)], fill="#5F6B76")
        bd.rectangle([(56, 20), (56 + round((tw - 80) * 0.38), 24)], fill=accent)
        canvas = Image.new("RGB", (tw, th + 44), "#141C24")
        canvas.paste(im, (0, 0)); canvas.paste(bar, (0, th))
        im = canvas
    else:
        tw = round(W * width) if im.width > im.height else round(H * 0.82 * im.width / im.height)
        th = round(im.height * tw / im.width)
        if th > H * 0.84:
            th = round(H * 0.84); tw = round(im.width * th / im.height)
        im = im.resize((tw, th), Image.LANCZOS)
        if im.width < 500:  # suavizar escalado agresivo
            im = im.filter(ImageFilter.SMOOTH)
    shadow, mask, pad = rounded_shadow(im)
    x = (W - im.width) // 2
    y = (H - im.height) // 2 - 8
    bg.alpha_composite(shadow, (x - pad, y - pad))
    bg.paste(im, (x, y), mask)
    return bg.convert("RGB")


def save(name, img):
    img.save(OUT / f"{name}.jpg", quality=84, optimize=True, progressive=True)
    print(name, img.size)


# --- capturas de productos publicados (alta resolución) --------------------
save("ciclo-genero", cover(CAP / "ejrlb-curso.png"))
save("ciclo-genero-cursos", cover(CAP / "ejrlb-home.png"))
save("wwf-lfa", cover(CAP / "wwf.png"))
save("atlas-undp", cover(CAP / "atlas.png"))
save("banco-experiencias", cover(CAP / "experiencias.png"))
save("infosegura", cover(CAP / "infosegura.png"))
save("campus-innovahub", cover(CAP / "campus.png"))
save("pueblos-indigenas", cover(CAP / "climaticas-genially.png", top=0.15))
save("ideas-en-accion", cover(CAP / "clinica-video.jpg", top=0.5))

# --- portadas y fotogramas del brochure (compuestos sobre fondo de marca) ---
save("hoja-ruta-juventud", framed(BRO / "p11_09_198x255.jpeg", PAL["blue"], PAL["coral"]))
save("mapeo-pgn", framed(BRO / "p11_06_196x255.jpeg", PAL["charcoal"], PAL["coral"]))
save("discapacidad", framed(BRO / "p14_09_248x137.jpeg", PAL["deep"], PAL["naranja"], width=0.7, mockup="video"))
save("inegi-genero", framed(BRO / "p19_18_317x176.jpeg", PAL["blue"], PAL["ocre"], width=0.76))
save("bolsa-agricola", framed(BRO / "p19_04_411x177.jpeg", PAL["charcoal"], PAL["keppel"], width=0.76))
save("conversaciones-climaticas", framed(BRO / "p19_07_412x176.jpeg", PAL["deep"], PAL["ocre"], width=0.76))
save("wwf-peaci", framed(BRO / "p18_07_317x176.jpeg", PAL["blue"], PAL["keppel"], width=0.76))
save("ciclo-genero-unidad", cover(CAP / "ejrlb-unidad.png"))
save("ciclo-genero-cuestionario", cover(CAP / "ejrlb-cuestionario.png"))
