"""Genera el mapa vectorial de los 13 países (proyección Equal Earth) a partir del
TopoJSON world-atlas 110m embebido en el proyecto Atlas.

Uso: python tools/make_map.py
Salida: src/partials/mapa.svg (se inserta inline con {{MAPA}}) y assets/img/mapa-13-paises.svg
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPO = Path(r"C:\wamp_3\www\atlas\assets\world110m.js")

PAISES = {
    "United States of America": ("Estados Unidos", (38.90, -77.04)),
    "Mexico": ("México", (19.43, -99.13)),
    "Guatemala": ("Guatemala", (14.63, -90.51)),
    "Honduras": ("Honduras", (14.07, -87.19)),
    "El Salvador": ("El Salvador", (13.69, -89.19)),
    "Costa Rica": ("Costa Rica", (9.93, -84.08)),
    "Panama": ("Panamá", (8.98, -79.52)),
    "Colombia": ("Colombia", (4.71, -74.07)),
    "Ecuador": ("Ecuador", (-0.18, -78.47)),
    "Venezuela": ("Venezuela", (10.49, -66.88)),
    "Eq. Guinea": ("Guinea Ecuatorial", (3.75, 8.78)),
    "Chile": ("Chile", (-33.45, -70.67)),
    "Brazil": ("Brasil", (-15.79, -47.88)),
}
LON0 = -40.0  # meridiano central

# --- TopoJSON -------------------------------------------------------------
src = TOPO.read_text(encoding="utf-8")
topo = json.loads(src[src.index("{"): src.rindex("}") + 1])
scale, translate = topo["transform"]["scale"], topo["transform"]["translate"]


def decode_arc(arc):
    x = y = 0
    pts = []
    for dx, dy in arc:
        x += dx
        y += dy
        pts.append((x * scale[0] + translate[0], y * scale[1] + translate[1]))
    return pts


ARCS = [decode_arc(a) for a in topo["arcs"]]


def ring_coords(ring):
    pts = []
    for idx in ring:
        arc = ARCS[idx] if idx >= 0 else list(reversed(ARCS[~idx]))
        if pts:
            arc = arc[1:]
        pts.extend(arc)
    return pts


def polygons(geom):
    if geom["type"] == "Polygon":
        return [[ring_coords(r) for r in geom["arcs"]]]
    if geom["type"] == "MultiPolygon":
        return [[ring_coords(r) for r in poly] for poly in geom["arcs"]]
    return []


# --- rotación, desdoblado y recorte en longitud -----------------------------
def unwrap(ring):
    out = []
    prev = None
    for lon, lat in ring:
        l = lon - LON0
        if prev is not None:
            while l - prev > 180:
                l -= 360
            while l - prev < -180:
                l += 360
        out.append([l, lat])
        prev = l
    mean = sum(p[0] for p in out) / len(out)
    if mean > 180:
        out = [[l - 360, la] for l, la in out]
    elif mean < -180:
        out = [[l + 360, la] for l, la in out]
    return out


def clip_lon(ring, xmin=-179.9, xmax=179.9):
    def clip(poly, inside, intersect):
        res = []
        for i, cur in enumerate(poly):
            prev = poly[i - 1]
            if inside(cur):
                if not inside(prev):
                    res.append(intersect(prev, cur))
                res.append(cur)
            elif inside(prev):
                res.append(intersect(prev, cur))
        return res

    def ix(a, b, x):
        t = (x - a[0]) / (b[0] - a[0])
        return [x, a[1] + t * (b[1] - a[1])]

    ring = clip(ring, lambda p: p[0] >= xmin, lambda a, b: ix(a, b, xmin))
    if not ring:
        return ring
    return clip(ring, lambda p: p[0] <= xmax, lambda a, b: ix(a, b, xmax))


# --- Equal Earth ------------------------------------------------------------
A1, A2, A3, A4 = 1.340264, -0.081106, 0.000893, 0.003796
M = math.sqrt(3) / 2


def project(lon, lat):
    lam, phi = math.radians(lon), math.radians(lat)
    th = math.asin(M * math.sin(phi))
    t2, t6 = th * th, th ** 6
    x = 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (9 * A4 * t6 * t2 + 7 * A3 * t6 + 3 * A2 * t2 + A1))
    y = A1 * th + A2 * th * t2 + A3 * t6 * th + A4 * t6 * t2 * th
    return x, -y


# --- recorte del área visible (América + África + Europa occidental) --------
W, H = 1000, 620
corners = [project(lon - LON0, lat) for lon in (-128, 52) for lat in (-57, 72)]
xs = [c[0] for c in corners] + [project(lon - LON0, 0)[0] for lon in (-128, 52)]
ys = [c[1] for c in corners] + [project(0, lat)[1] for lat in (-57, 72)]
minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
S = min(W / (maxx - minx), H / (maxy - miny))
OX = (W - (maxx - minx) * S) / 2
OY = (H - (maxy - miny) * S) / 2


def to_svg(x, y):
    return (x - minx) * S + OX, (y - miny) * S + OY


def path_for(polys):
    d = []
    for poly in polys:
        for ring in poly:
            r = clip_lon(unwrap(ring))
            if len(r) < 3:
                continue
            pts = [to_svg(*project(l, la)) for l, la in r]
            d.append("M" + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    return "".join(d)


land, marcados, puntos = [], [], []
for geom in topo["objects"]["countries"]["geometries"]:
    name = geom["properties"]["name"]
    if name == "Antarctica":
        continue
    d = path_for(polygons(geom))
    if not d:
        continue
    if name in PAISES:
        etiqueta, (lat, lon) = PAISES[name]
        marcados.append(f'<path class="pais" d="{d}"><title>{etiqueta}</title></path>')
        x, y = to_svg(*project(lon - LON0, lat))
        puntos.append(
            f'<g class="punto" transform="translate({x:.1f} {y:.1f})"><circle class="halo" r="9"/>'
            f'<circle class="dot" r="4"/><title>{etiqueta}</title></g>'
        )
    else:
        land.append(f'<path d="{d}"/>')

svg = f'''<svg class="mapa" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="mapa-titulo">
<title id="mapa-titulo">Mapa de los 13 países donde ha trabajado Innovahub en América y África</title>
<defs>
  <pattern id="mapa-grid" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" r="1.2" fill="currentColor" opacity=".18"/></pattern>
</defs>
<rect width="{W}" height="{H}" fill="url(#mapa-grid)"/>
<g class="tierra">{"".join(land)}</g>
<g class="marcados">{"".join(marcados)}</g>
<g class="puntos">{"".join(puntos)}</g>
</svg>
'''
(ROOT / "src" / "partials" / "mapa.svg").write_text(svg, encoding="utf-8")
(ROOT / "assets" / "img" / "mapa-13-paises.svg").write_text(svg, encoding="utf-8")
print("mapa:", len(land), "países base,", len(marcados), "marcados,", len(svg) // 1024, "KB")
