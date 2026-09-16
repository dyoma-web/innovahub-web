"""Ilustraciones isométricas voxel en SVG (línea gráfica del manual: escenarios
geométricos por bloques, paleta de marca, fondo transparente).

Uso: python tools/voxel.py
Salida: assets/img/ilustraciones/*.svg
"""
import colorsys
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img" / "ilustraciones"
OUT.mkdir(parents=True, exist_ok=True)

PAL = {
    "coral": "#DA5A49", "naranja": "#DD7A3E", "ocre": "#EAC44C", "keppel": "#45AD98",
    "charcoal": "#334D5C", "blue": "#363F4E", "steel": "#396D8A", "blanco": "#FFFFFF",
    "gris": "#E7EAEE", "piel1": "#F2C9A8", "piel2": "#C98B62", "piel3": "#8D5A3B",
    "pelo1": "#2B2B2B", "pelo2": "#6B3E2E", "pelo3": "#D9A441", "pelo4": "#4A3A6B",
    "pantalla": "#1E2F3D", "luz": "#9FE8D6",
}


def shade(hexcol, f):
    hexcol = hexcol.lstrip("#")
    r, g, b = (int(hexcol[i:i + 2], 16) / 255 for i in (0, 2, 4))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l * f))
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#%02X%02X%02X" % (round(r * 255), round(g * 255), round(b * 255))


class Scene:
    def __init__(self, size=22):
        self.s = size
        self.vox = {}   # (x,y,z) -> color
        self.extra = []  # svg extra (dibujado encima)

    # --- primitivas ---
    def cube(self, x, y, z, color):
        self.vox[(x, y, z)] = color

    def box(self, x0, x1, y0, y1, z0, z1, color):
        for x in range(x0, x1):
            for y in range(y0, y1):
                for z in range(z0, z1):
                    self.cube(x, y, z, color)

    def person(self, x, y, z, camisa, piel="piel1", pelo="pelo1", alto=True):
        """Figura 1x1 de base: piernas, torso, cabeza, pelo."""
        self.cube(x, y, z, "charcoal")           # piernas
        self.cube(x, y, z + 1, camisa)           # torso
        if alto:
            self.cube(x, y, z + 2, camisa)
            zc = z + 3
        else:
            zc = z + 2
        self.cube(x, y, zc, piel)                # cabeza
        self.cube(x, y, zc + 1, pelo)            # pelo

    def person_big(self, x, y, z, camisa, piel="piel1", pelo="pelo1", largo=False):
        """Personaje 2x1 de base con cara: piernas, torso, brazos, cabeza y pelo."""
        self.cube(x, y, z, "charcoal"); self.cube(x + 1, y, z, "charcoal")          # piernas
        for k in (1, 2):
            self.cube(x, y, z + k, camisa); self.cube(x + 1, y, z + k, camisa)      # torso
        self.cube(x - 1, y, z + 2, camisa); self.cube(x + 2, y, z + 2, camisa)      # hombros
        self.cube(x - 1, y, z + 1, piel); self.cube(x + 2, y, z + 1, piel)          # manos
        for k in (3, 4):
            self.cube(x, y, z + k, piel); self.cube(x + 1, y, z + k, piel)          # cabeza
        self.cube(x, y, z + 5, pelo); self.cube(x + 1, y, z + 5, pelo)              # pelo arriba
        self.cube(x, y - 1, z + 4, pelo); self.cube(x + 1, y - 1, z + 4, pelo)      # pelo atrás
        if largo:
            self.cube(x, y - 1, z + 3, pelo); self.cube(x + 1, y - 1, z + 3, pelo)
            self.cube(x, y - 1, z + 2, pelo); self.cube(x + 1, y - 1, z + 2, pelo)
        # ojos y boca sobre la cara frontal (cara "left" del cubo, y+1 vacío)
        self.dots = getattr(self, "dots", [])
        self.dots.append((x, y, z + 4, 0.55, 0.45, 0.16, "#2B2B2B"))
        self.dots.append((x + 1, y, z + 4, 0.45, 0.45, 0.16, "#2B2B2B"))
        self.dots.append((x, y, z + 3, 0.78, 0.35, 0.10, "#B5533F"))
        self.dots.append((x + 1, y, z + 3, 0.22, 0.35, 0.10, "#B5533F"))

    def screen(self, x, y, z, w, h, marco="charcoal", pixels=None, along="x"):
        """Pantalla delgada (1 de fondo) con píxeles de colores en la cara frontal."""
        for i in range(w):
            for k in range(h):
                if along == "x":
                    self.cube(x + i, y, z + k, marco)
                else:
                    self.cube(x, y + i, z + k, marco)
        self.pixels = getattr(self, "pixels", [])
        if pixels:
            for (i, k, c) in pixels:
                self.pixels.append((x, y, z, i, k, c, along))

    # --- proyección ---
    def proj(self, x, y, z):
        s = self.s
        return ((x - y) * s * math.cos(math.radians(30)), (x + y) * s * 0.5 - z * s)

    def render(self, width, height, ox, oy, shadow=None, extra_before=""):
        s = self.s
        c30 = s * math.cos(math.radians(30))
        parts = []
        # orden de pintado
        for (x, y, z), cname in sorted(self.vox.items(), key=lambda kv: (kv[0][0] + kv[0][1] + kv[0][2], kv[0][2])):
            base = PAL.get(cname, cname)
            px, py = self.proj(x, y, z)
            px += ox
            py += oy
            # caras: top, left(-y face visible), right(+x face visible)
            top = [(px, py - s), (px + c30, py - s + s * 0.5), (px, py), (px - c30, py - s + s * 0.5)]
            left = [(px - c30, py - s + s * 0.5), (px, py), (px, py + s), (px - c30, py + s * 0.5)]
            right = [(px, py), (px + c30, py - s + s * 0.5), (px + c30, py + s * 0.5), (px, py + s)]
            # ocultar caras cubiertas por vecinos
            if (x, y, z + 1) not in self.vox:
                parts.append(poly(top, shade(base, 1.18)))
            if (x, y + 1, z) not in self.vox:
                parts.append(poly(left, base))
            if (x + 1, y, z) not in self.vox:
                parts.append(poly(right, shade(base, 0.78)))
        # píxeles de pantallas (sobre la cara frontal = cara "left", y+1 vacío)
        for (x, y, z, i, k, c, along) in getattr(self, "pixels", []):
            if along == "x":
                px, py = self.proj(x + i, y, z + k)
            else:
                px, py = self.proj(x, y + i, z + k)
            px += ox
            py += oy
            m = 0.22 * s
            if along == "x":
                face = [(px - c30, py - s + s * 0.5), (px, py), (px, py + s), (px - c30, py + s * 0.5)]
            else:
                face = [(px, py), (px + c30, py - s + s * 0.5), (px + c30, py + s * 0.5), (px, py + s)]
            parts.append(poly(inset(face, 0.18), PAL.get(c, c)))
        # detalles (ojos, boca) sobre la cara frontal
        for (x, y, z, u, v, size, color) in getattr(self, "dots", []):
            px, py = self.proj(x, y, z)
            px += ox
            py += oy
            a, b, c, d = (px - c30, py - s + s * 0.5), (px, py), (px, py + s), (px - c30, py + s * 0.5)
            def bil(uu, vv):
                # u: horizontal (0 izquierda→1 derecha), v: vertical (0 arriba→1 abajo)
                top = (a[0] + (b[0] - a[0]) * uu, a[1] + (b[1] - a[1]) * uu)
                bot = (d[0] + (c[0] - d[0]) * uu, d[1] + (c[1] - d[1]) * uu)
                return (top[0] + (bot[0] - top[0]) * vv, top[1] + (bot[1] - top[1]) * vv)
            h = size / 2
            face = [bil(u - h, v - h), bil(u + h, v - h), bil(u + h, v + h), bil(u - h, v + h)]
            parts.append(poly(face, color))
        body = "".join(parts)
        sh = ""
        if shadow:
            cx, cy, rx, ry = shadow
            sh = f'<ellipse cx="{cx + ox:.1f}" cy="{cy + oy:.1f}" rx="{rx}" ry="{ry}" fill="#000" opacity=".18"/>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
                f'{sh}{extra_before}{body}{"".join(self.extra)}</svg>')


def poly(pts, fill):
    return '<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="{fill}"/>'


def inset(face, f):
    cx = sum(p[0] for p in face) / 4
    cy = sum(p[1] for p in face) / 4
    return [(cx + (x - cx) * (1 - f), cy + (y - cy) * (1 - f)) for x, y in face]


def nodes_network(points, color="#FFFFFF", r=5, opacity=.9):
    """Nodos y aristas (motivo del isologo)."""
    out = []
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if (i + j) % 3 == 0 or j == i + 1:
                (x1, y1), (x2, y2) = points[i], points[j]
                out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.2" opacity=".45"/>')
    cols = ["#DD7A3E", "#EAC44C", "#45AD98", "#DA5A49", "#FFFFFF"]
    for k, (x, y) in enumerate(points):
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{cols[k % len(cols)]}" opacity="{opacity}"/>')
    return "".join(out)


# ---------------------------------------------------------------------------
# Escena 1: hub de conocimiento (hero del home)
# ---------------------------------------------------------------------------
def hero():
    sc = Scene(22)
    # plataforma flotante 12x12, 2 niveles
    sc.box(0, 12, 0, 12, 0, 1, "blue")
    sc.box(1, 11, 1, 11, 1, 2, "charcoal")
    # baldosas de color en la plataforma
    for (x, y, c) in [(2, 2, "keppel"), (9, 2, "ocre"), (2, 9, "coral"), (9, 9, "naranja"), (5, 5, "steel"), (6, 6, "steel")]:
        sc.cube(x, y, 1, c)
    # torre central (keppel) con pantalla
    sc.box(4, 8, 4, 8, 2, 6, "keppel")
    sc.box(5, 7, 5, 7, 6, 8, "keppel")
    sc.cube(6, 6, 8, "ocre")
    # pantalla grande a la izquierda
    pix = [(i, k, "luz" if (i + k) % 3 else "ocre") for i in range(1, 5) for k in range(1, 3)]
    pix += [(1, 3, "naranja"), (2, 3, "naranja"), (3, 3, "keppel"), (4, 3, "coral")]
    sc.screen(1, 3, 2, 6, 5, marco="pantalla", pixels=pix, along="x")
    # stacks de conocimiento (libros / cubos)
    sc.box(9, 11, 3, 5, 2, 5, "naranja")
    sc.cube(9, 3, 5, "ocre")
    sc.box(9, 11, 8, 10, 2, 4, "coral")
    sc.box(2, 4, 9, 11, 2, 4, "ocre")
    sc.cube(2, 9, 4, "keppel")
    # personas
    sc.person(8, 6, 2, "naranja", "piel2", "pelo1")
    sc.person(3, 7, 2, "coral", "piel1", "pelo3")
    sc.person(6, 10, 2, "keppel", "piel3", "pelo1")
    sc.person(10, 10, 2, "ocre", "piel1", "pelo4", alto=False)
    # cubos flotantes
    for (x, y, z, c) in [(1, 1, 7, "ocre"), (11, 1, 8, "keppel"), (11, 11, 9, "coral"), (0, 11, 6, "naranja"), (7, 1, 10, "blanco")]:
        sc.cube(x, y, z, c)
    W, H = 640, 560
    ox, oy = W / 2, 330
    net = nodes_network([(90, 120), (170, 60), (300, 40), (470, 70), (560, 150), (520, 250), (120, 230)])
    return sc.render(W, H, ox, oy, shadow=(0, 190, 250, 40), extra_before=net)


# ---------------------------------------------------------------------------
# Escena 2: aula virtual (página de servicio Formación virtual)
# ---------------------------------------------------------------------------
def aula():
    sc = Scene(24)
    sc.box(0, 11, 0, 9, 0, 1, "blue")
    sc.box(1, 10, 1, 8, 1, 2, "charcoal")
    for (x, y, c) in [(2, 2, "naranja"), (8, 2, "ocre"), (2, 6, "keppel"), (8, 6, "coral")]:
        sc.cube(x, y, 1, c)
    # pantalla / tablero grande
    pix = [(i, k, "luz") for i in range(1, 7) for k in range(1, 2)]
    pix += [(1, 2, "ocre"), (2, 2, "ocre"), (3, 2, "ocre"), (5, 2, "naranja"), (6, 2, "naranja")]
    pix += [(1, 3, "keppel"), (2, 3, "keppel"), (4, 3, "coral"), (5, 3, "coral"), (6, 3, "coral")]
    sc.screen(1, 1, 2, 8, 5, marco="pantalla", pixels=pix, along="x")
    # escritorios con laptops
    for (x, y) in [(3, 5), (6, 5), (3, 7), (6, 7)]:
        sc.box(x, x + 2, y, y + 1, 2, 3, "gris")
        sc.cube(x, y, 3, "steel")
    # estudiantes
    sc.person(4, 4, 2, "naranja", "piel2", "pelo1", alto=False)
    sc.person(7, 4, 2, "keppel", "piel1", "pelo3", alto=False)
    sc.person(4, 6, 2, "coral", "piel3", "pelo1", alto=False)
    sc.person(7, 6, 2, "ocre", "piel1", "pelo4", alto=False)
    # tutor
    sc.person(9, 2, 2, "keppel", "piel2", "pelo2")
    # cubos flotantes con "insignia"
    for (x, y, z, c) in [(0, 8, 6, "ocre"), (10, 0, 7, "keppel"), (10, 8, 8, "coral")]:
        sc.cube(x, y, z, c)
    W, H = 620, 520
    return sc.render(W, H, W / 2, 320, shadow=(0, 165, 240, 38))


# ---------------------------------------------------------------------------
# Escena 3: equipo (Nosotros)
# ---------------------------------------------------------------------------
def equipo():
    sc = Scene(24)
    sc.box(0, 11, 0, 11, 0, 1, "blue")
    sc.box(1, 10, 1, 10, 1, 2, "charcoal")
    # mesa central
    sc.box(4, 7, 4, 7, 2, 3, "gris")
    sc.cube(5, 5, 3, "ocre")
    conf = [((2, 2), "naranja", "piel1", "pelo1"), ((5, 2), "keppel", "piel2", "pelo3"), ((8, 2), "coral", "piel3", "pelo1"),
            ((2, 5), "ocre", "piel2", "pelo4"), ((8, 5), "steel", "piel1", "pelo2"),
            ((2, 8), "keppel", "piel3", "pelo1"), ((5, 8), "coral", "piel1", "pelo3"), ((8, 8), "naranja", "piel2", "pelo1")]
    for (x, y), c, p, h in conf:
        sc.person(x, y, 2, c, p, h, alto=(x + y) % 2 == 0)
    sc.s = 24
    for (x, y, z, c) in [(0, 10, 6, "ocre"), (10, 0, 7, "keppel"), (10, 10, 8, "coral"), (0, 0, 9, "naranja")]:
        sc.cube(x, y, z, c)
    W, H = 620, 520
    return sc.render(W, H, W / 2, 330, shadow=(0, 165, 250, 40))


# ---------------------------------------------------------------------------
# Avatares (Nosotros): una figura por archivo
# ---------------------------------------------------------------------------
def avatar(camisa, piel, pelo, largo=False):
    sc = Scene(22)
    sc.box(-1, 5, 0, 3, 0, 1, "blue")
    sc.person_big(1, 1, 1, camisa, piel, pelo, largo=largo)
    W, H = 240, 260
    return sc.render(W, H, W / 2 - 10, 205)


if __name__ == "__main__":
    (OUT / "hero-hub.svg").write_text(hero(), encoding="utf-8")
    (OUT / "aula-virtual.svg").write_text(aula(), encoding="utf-8")
    (OUT / "equipo.svg").write_text(equipo(), encoding="utf-8")
    avatars = [("naranja", "piel2", "pelo1", False), ("keppel", "piel1", "pelo3", True), ("coral", "piel3", "pelo1", False),
               ("ocre", "piel1", "pelo4", True), ("steel", "piel2", "pelo2", False), ("keppel", "piel3", "pelo1", True)]
    for i, a in enumerate(avatars, 1):
        (OUT / f"avatar-{i}.svg").write_text(avatar(*a), encoding="utf-8")
    print("ok", sorted(p.name for p in OUT.iterdir()))
