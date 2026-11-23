"""Utilidades de dibujo: SVG -> PNG con rsvg-convert + postproceso con PIL."""
import math
import os
import random
import subprocess

import numpy as np
from PIL import Image, ImageFilter

W, H = 1920, 1080
INK = "#05070c"
# Rutas relativas al repositorio (funciona igual en Windows, macOS y Linux).
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
OUT = os.path.join(RAIZ, "game", "images")
ARTE = os.path.join(AQUI, "_trabajo")  # imágenes intermedias (no van al juego)
os.makedirs(ARTE, exist_ok=True)


def doc(body, defs="", w=W, h=H):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{COMMON_DEFS}{defs}</defs>{body}</svg>')


COMMON_DEFS = """
<filter id="b2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="b4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="b8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="b16" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="16"/></filter>
<filter id="b30" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="30"/></filter>
<filter id="b60" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="60"/></filter>
<radialGradient id="glowSodio"><stop offset="0" stop-color="#ffe2a8" stop-opacity="1"/><stop offset="0.25" stop-color="#ffb35c" stop-opacity="0.55"/><stop offset="1" stop-color="#ff8a2a" stop-opacity="0"/></radialGradient>
<radialGradient id="glowFrio"><stop offset="0" stop-color="#eaf6ff" stop-opacity="1"/><stop offset="0.3" stop-color="#9fd0ff" stop-opacity="0.45"/><stop offset="1" stop-color="#5aa0e0" stop-opacity="0"/></radialGradient>
<radialGradient id="glowVela"><stop offset="0" stop-color="#fff1c4" stop-opacity="1"/><stop offset="0.3" stop-color="#ffb85a" stop-opacity="0.5"/><stop offset="1" stop-color="#ff7a1a" stop-opacity="0"/></radialGradient>
<radialGradient id="pozoSodio" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#f3a35a" stop-opacity="0.55"/><stop offset="1" stop-color="#f3a35a" stop-opacity="0"/></radialGradient>
<radialGradient id="pozoFrio" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#a9d4f0" stop-opacity="0.45"/><stop offset="1" stop-color="#a9d4f0" stop-opacity="0"/></radialGradient>
"""


def render(svg, path, w=None, h=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp.svg"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(svg)
    cmd = ["rsvg-convert", "-o", path]
    if w:
        cmd += ["-w", str(w)]
    if h:
        cmd += ["-h", str(h)]
    cmd.append(tmp)
    subprocess.run(cmd, check=True)
    os.remove(tmp)


def post(path, grain=7.0, vignette=0.55, tint=None, seed=1, out=None, sepia=False, gray=False):
    """Grano de película, viñeta y gradación de color (fondos/CG opacos)."""
    rng = np.random.default_rng(seed)
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    if gray or sepia:
        lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11
        if sepia:
            a = np.stack([lum * 1.07 + 10, lum * 0.92 + 4, lum * 0.72], -1)
        else:
            a = np.stack([lum, lum, lum], -1)
    if tint is not None:
        # tint: (sombras_rgb, luces_rgb) mezcla suave según luminancia
        lum = (a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11) / 255.0
        sh = np.array(tint[0], np.float32)
        hi = np.array(tint[1], np.float32)
        t = lum[..., None]
        grade = sh * (1 - t) + hi * t
        a = a * 0.86 + grade * 0.14
    if vignette:
        yy, xx = np.mgrid[0:h, 0:w]
        d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
        v = 1 - vignette * np.clip((d - 0.45) / 0.95, 0, 1) ** 1.6
        a *= v[..., None]
    if grain:
        n = rng.normal(0, grain, (h // 2 + 1, w // 2 + 1)).astype(np.float32)
        n = np.kron(n, np.ones((2, 2), np.float32))[:h, :w]
        n = Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))
        n = np.asarray(n).astype(np.float32) - 128
        a += n[..., None] * 1.0
    a = np.clip(a, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(out or path, optimize=True)


def post_sprite(path, ghost=False, fade_bottom=False, glow=False, grain=4.0, seed=3):
    """Postproceso para sprites con transparencia."""
    rng = np.random.default_rng(seed)
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    if grain:
        n = rng.normal(0, grain, (h, w)).astype(np.float32)
        a[..., :3] += n[..., None]
    if ghost:
        lum = a[..., 0] * 0.3 + a[..., 1] * 0.59 + a[..., 2] * 0.11
        cold = np.stack([lum * 0.93, lum * 0.99, lum * 1.08], -1)
        a[..., :3] = a[..., :3] * 0.72 + cold * 0.28
    if fade_bottom:
        yy = np.arange(h)[:, None].astype(np.float32)
        f = np.clip(1 - (yy - h * 0.80) / (h * 0.20), 0, 1)
        a[..., 3] *= f
    a = np.clip(a, 0, 255).astype(np.uint8)
    out = Image.fromarray(a, "RGBA")
    if glow:
        alpha = out.split()[3]
        g = alpha.filter(ImageFilter.GaussianBlur(18))
        g = g.point(lambda v: int(v * 0.45))
        glow_im = Image.new("RGBA", out.size, (190, 215, 255, 0))
        glow_im.putalpha(g)
        base = Image.new("RGBA", out.size, (0, 0, 0, 0))
        base = Image.alpha_composite(base, glow_im)
        out = Image.alpha_composite(base, out)
    out.save(path, optimize=True)


# ---------------------------------------------------------------------------
#  Elementos reutilizables
# ---------------------------------------------------------------------------

def estrellas(n, seed, y_max=600, w=W, dens_top=True):
    rnd = random.Random(seed)
    s = []
    for _ in range(n):
        x = rnd.uniform(0, w)
        y = rnd.uniform(0, y_max) ** 1.0
        if dens_top:
            y = y_max * (rnd.random() ** 1.6)
        r = rnd.choice([0.6, 0.8, 0.9, 1.1, 1.3, 1.6, 2.2])
        o = rnd.uniform(0.25, 1.0)
        col = rnd.choice(["#ffffff", "#dfe9ff", "#fff3dc", "#cfe0ff"])
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}" opacity="{o:.2f}"/>')
        if r > 1.5:
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*4}" fill="{col}" opacity="{o*0.18:.2f}" filter="url(#b2)"/>')
    return "".join(s)


def via_lactea(cx, cy, rx, ry, rot, seed):
    rnd = random.Random(seed)
    parts = [f'<g transform="rotate({rot} {cx} {cy})" opacity="0.55">',
             f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#2a3a5c" filter="url(#b60)"/>',
             f'<ellipse cx="{cx}" cy="{cy}" rx="{rx*0.7}" ry="{ry*0.35}" fill="#41557c" filter="url(#b30)" opacity="0.7"/>']
    for _ in range(420):
        x = rnd.gauss(cx, rx * 0.5)
        y = rnd.gauss(cy, ry * 0.35)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.choice([0.5,0.7,0.9])}" fill="#e8eeff" opacity="{rnd.uniform(0.2,0.8):.2f}"/>')
    for _ in range(7):
        x = rnd.gauss(cx, rx * 0.4)
        y = rnd.gauss(cy, ry * 0.15)
        parts.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(40,120):.0f}" ry="{rnd.uniform(8,20):.0f}" fill="#05070c" opacity="0.5" filter="url(#b16)"/>')
    parts.append('</g>')
    return "".join(parts)


def cerro(y_base, amp, seed, color, w=W, rough=1.0, rim=None, steps=90):
    rnd = random.Random(seed)
    pts = []
    y = 0.0
    vals = []
    for i in range(steps + 1):
        y += rnd.gauss(0, 1) * rough
        vals.append(y)
    # suavizar y normalizar
    vals = np.convolve(vals, np.ones(5) / 5, mode="same")
    vals = (vals - vals.min()) / (vals.max() - vals.min() + 1e-6)
    # forma general de loma
    for i, v in enumerate(vals):
        x = w * i / steps
        bump = math.sin(math.pi * i / steps * rnd.uniform(0.9, 1.0)) * 0.3
        pts.append((x, y_base - amp * (v * 0.75 + bump)))
    d = f"M0,{H+10} " + " ".join(f"L{x:.1f},{yy:.1f}" for x, yy in pts) + f" L{w},{H+10} Z"
    out = f'<path d="{d}" fill="{color}"/>'
    if rim:
        dl = "M" + " L".join(f"{x:.1f},{yy:.1f}" for x, yy in pts)
        out += f'<path d="{dl}" fill="none" stroke="{rim}" stroke-width="2" opacity="0.5"/>'
    return out


def farol(x, yg, alto, tipo="sodio", escala=1.0, glow=True, poste="#06080d"):
    s = escala
    g = "glowSodio" if tipo == "sodio" else "glowFrio"
    pozo = "pozoSodio" if tipo == "sodio" else "pozoFrio"
    top = yg - alto
    out = []
    out.append(f'<ellipse cx="{x}" cy="{yg+6*s}" rx="{260*s}" ry="{55*s}" fill="url(#{pozo})"/>')
    out.append(f'<rect x="{x-5*s}" y="{top}" width="{10*s}" height="{alto}" fill="{poste}"/>')
    out.append(f'<rect x="{x-11*s}" y="{yg-30*s}" width="{22*s}" height="{30*s}" fill="{poste}"/>')
    # farol colonial
    out.append(f'<path d="M{x-22*s},{top} L{x+22*s},{top} L{x+15*s},{top+38*s} L{x-15*s},{top+38*s} Z" fill="#ffd79a"/>')
    out.append(f'<path d="M{x-28*s},{top} L{x+28*s},{top} L{x},{top-22*s} Z" fill="{poste}"/>')
    out.append(f'<rect x="{x-17*s}" y="{top+36*s}" width="{34*s}" height="{6*s}" fill="{poste}"/>')
    if glow:
        out.append(f'<circle cx="{x}" cy="{top+18*s}" r="{150*s}" fill="url(#{g})" opacity="0.9"/>')
        out.append(f'<circle cx="{x}" cy="{top+18*s}" r="{40*s}" fill="url(#{g})"/>')
    return "".join(out)


def pimiento(cx, ytop, ancho, alto, seed, base="#0a130f", hoja="#14231b", luz=None, tronco_y=None, densidad=1.0, lado_luz=1, luz_x=None):
    """Pimiento (Schinus molle): copa ancha hecha de racimos colgantes (como sauce) y tronco retorcido."""
    rnd = random.Random(seed)
    out = []
    ty = tronco_y if tronco_y is not None else ytop + alto
    tw = ancho * 0.06
    # tronco retorcido con dos brazos
    out.append(f'<path d="M{cx-tw*1.3},{ty} C{cx-tw*0.6},{ty-alto*0.2} {cx-tw*1.6},{ty-alto*0.35} {cx-tw*0.4},{ytop+alto*0.42} '
               f'L{cx+tw*0.9},{ytop+alto*0.42} C{cx+tw*0.3},{ty-alto*0.38} {cx+tw*1.4},{ty-alto*0.2} {cx+tw*1.6},{ty} Z" fill="#060708"/>')
    out.append(f'<path d="M{cx-tw*1.3},{ty} C{cx-tw*0.6},{ty-alto*0.2} {cx-tw*1.6},{ty-alto*0.35} {cx-tw*0.4},{ytop+alto*0.42}" stroke="#2a2f36" stroke-width="3" fill="none" opacity="0.6"/>')
    for k in range(6):
        ang = rnd.uniform(-1, 1)
        x2 = cx + ang * ancho * 0.42
        y2 = ytop + alto * rnd.uniform(0.10, 0.28)
        out.append(f'<path d="M{cx+rnd.uniform(-tw,tw):.0f},{ytop+alto*0.45:.0f} Q{(cx+x2)/2+rnd.uniform(-60,60):.0f},{y2+alto*0.12:.0f} {x2:.0f},{y2:.0f}" '
                   f'stroke="#060708" stroke-width="{rnd.uniform(8,18)*ancho/900:.0f}" fill="none" stroke-linecap="round"/>')

    def racimo(x, y, w, h, col, op=1.0):
        # gota colgante con borde inferior deshilachado
        n = max(6, int(w / 9))
        pts = []
        for i in range(n + 1):
            t = i / n
            xx = x - w / 2 + w * t
            prof = math.sin(math.pi * t) ** 0.6
            yy = y + h * (0.55 + 0.45 * prof) + rnd.uniform(-0.12, 0.10) * h
            pts.append((xx, yy))
            if i < n:
                pts.append((xx + w / n * 0.5, yy - rnd.uniform(0.05, 0.18) * h))
        d = f"M{x - w/2:.1f},{y + h*0.25:.1f} Q{x - w*0.45:.1f},{y - h*0.1:.1f} {x:.1f},{y - h*0.05:.1f} Q{x + w*0.45:.1f},{y - h*0.1:.1f} {x + w/2:.1f},{y + h*0.25:.1f} "
        d += " ".join(f"L{a:.1f},{b:.1f}" for a, b in reversed(pts)) + " Z"
        return f'<path d="{d}" fill="{col}" opacity="{op:.2f}"/>'

    capas = [(base, 1.0, 0.0), (hoja, 0.92, 0.04)]
    # cúpula superior
    for k in range(int(16 * densidad)):
        u = rnd.uniform(-0.85, 0.85)
        ex = cx + u * ancho * 0.5
        ey = ytop + alto * (0.07 + 0.30 * u * u)
        out.append(f'<ellipse cx="{ex:.0f}" cy="{ey:.0f}" rx="{ancho*rnd.uniform(0.07,0.12):.0f}" ry="{alto*rnd.uniform(0.05,0.08):.0f}" fill="{base}"/>')
    nrac = int(150 * densidad)
    fondo = ytop + alto * 0.86
    for ci, (col, op, dy) in enumerate(capas):
        for k in range(nrac):
            u = rnd.uniform(-1, 1)
            x = cx + u * ancho * 0.5 * (0.92 + 0.08 * rnd.random())
            y = ytop + alto * (0.04 + 0.30 * u * u + 0.06 * rnd.random() + dy)
            w = ancho * rnd.uniform(0.035, 0.085)
            h = (fondo - y) * rnd.uniform(0.55, 1.05)
            if abs(u) < 0.18:
                h *= rnd.uniform(0.45, 0.8)   # deja ver el tronco
            c = col
            if luz is not None:
                lx = luz_x if luz_x is not None else cx + lado_luz * ancho * 0.5
                dist = abs(x - lx) / ancho
                if dist < 0.35 and rnd.random() < (0.40 - dist * 1.1) and ci == 1:
                    c = luz
                    op = 0.7
            out.append(racimo(x, y, w, h, c, op))
    # hebras finas en el borde inferior
    for k in range(int(220 * densidad)):
        u = rnd.uniform(-1, 1)
        caida = (1 - abs(u) ** 1.6)
        x0 = cx + u * ancho * 0.48
        y0 = ytop + alto * rnd.uniform(0.55, 0.88)
        largo = alto * rnd.uniform(0.04, 0.16)
        sway = rnd.uniform(-8, 8)
        col = rnd.choice([base, hoja])
        out.append(f'<path d="M{x0:.1f},{y0:.1f} q{sway/2:.1f},{largo/2:.1f} {sway:.1f},{largo:.1f}" stroke="{col}" stroke-width="{rnd.uniform(1.2,3):.1f}" '
                   f'stroke-dasharray="3 2" fill="none" stroke-linecap="round"/>')
    return "".join(out)


def ciprés(x, yb, alto, ancho, color="#070b0c", seed=0):
    rnd = random.Random(seed)
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        y = yb - alto * t
        half = ancho * (math.sin(math.pi * (0.15 + 0.85 * (1 - t))) * 0.5 + 0.08) * (1 - t * 0.55)
        pts.append((x - half * rnd.uniform(0.85, 1.1), y))
    pts2 = []
    for i in range(n, -1, -1):
        t = i / n
        y = yb - alto * t
        half = ancho * (math.sin(math.pi * (0.15 + 0.85 * (1 - t))) * 0.5 + 0.08) * (1 - t * 0.55)
        pts2.append((x + half * rnd.uniform(0.85, 1.1), y))
    d = "M" + " L".join(f"{a:.0f},{b:.0f}" for a, b in pts + [(x, yb - alto - 18)] + pts2) + " Z"
    return f'<path d="{d}" fill="{color}"/>'


def texto(x, y, s, size, fill="#fff", font="DejaVu Serif", weight="normal", style="normal", anchor="middle",
          spacing=0, opacity=1, extra=""):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" font-style="{style}" '
            f'text-anchor="{anchor}" fill="{fill}" letter-spacing="{spacing}" opacity="{opacity}" {extra}>{s}</text>')


def garabatos(x, y, ancho, lineas, alto_linea, seed, color="#2a2a3a", sw=2.2, op=0.85):
    """Líneas de 'letra manuscrita' ilegible."""
    rnd = random.Random(seed)
    out = []
    for i in range(lineas):
        yy = y + i * alto_linea
        largo = ancho * (rnd.uniform(0.55, 1.0) if i < lineas - 1 else rnd.uniform(0.25, 0.5))
        xx = x
        d = f"M{xx:.1f},{yy:.1f}"
        while xx < x + largo:
            palabra = rnd.uniform(30, 90)
            fin = min(xx + palabra, x + largo)
            while xx < fin:
                dx = rnd.uniform(5, 10)
                up = rnd.uniform(-9, -3) if rnd.random() < 0.8 else rnd.uniform(-22, -14)
                d += f" q{dx/2:.1f},{up:.1f} {dx:.1f},0"
                xx += dx
            xx += rnd.uniform(10, 18)
            d += f" M{xx:.1f},{yy + rnd.uniform(-1,1):.1f}"
        out.append(f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="none" stroke-linecap="round" opacity="{op}"/>')
    return "".join(out)
