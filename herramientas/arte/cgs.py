"""Escenas especiales (CG), título y menús de LA CHAQUETA."""
import math
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

from lib import *
import fondos
import sprites

CG = OUT + "/cg"
GUI = os.path.join(RAIZ, "game", "gui")
TMP = os.path.join(ARTE, "tmp")
os.makedirs(TMP, exist_ok=True)
os.makedirs(CG, exist_ok=True)
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_C = "/usr/share/fonts/truetype/dejavu/DejaVuSerifCondensed-Italic.ttf"


def sepia(im, fuerza=1.0):
    g = ImageOps.grayscale(im.convert("RGB"))
    a = np.asarray(g).astype(np.float32)
    rgb = np.stack([a * 1.07 + 14, a * 0.93 + 6, a * 0.74], -1)
    out = Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))
    if fuerza < 1:
        out = Image.blend(im.convert("RGB"), out, fuerza)
    return out


def bn(im):
    g = ImageOps.grayscale(im.convert("RGB"))
    g = ImageOps.autocontrast(g, cutoff=1)
    return Image.merge("RGB", (g, g, g))


def grano(im, s=10, seed=0):
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    a += rng.normal(0, s, a.shape[:2])[..., None]
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def rayas(im, n=30, seed=0, color=(235, 225, 205)):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(im, "RGBA")
    w, h = im.size
    for _ in range(n):
        x = rnd.uniform(0, w)
        y0 = rnd.uniform(0, h)
        L = rnd.uniform(20, h * 0.6)
        d.line([(x, y0), (x + rnd.uniform(-6, 6), y0 + L)], fill=color + (rnd.randint(25, 70),), width=1)
    for _ in range(n * 2):
        x, y = rnd.uniform(0, w), rnd.uniform(0, h)
        r = rnd.uniform(0.5, 2.5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (rnd.randint(30, 90),))
    return im


def vineta(im, f=0.6):
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    v = 1 - f * np.clip((d - 0.4) / 0.9, 0, 1) ** 1.5
    return Image.fromarray(np.clip(a * v[..., None], 0, 255).astype(np.uint8))


def guardar(im, path, grain=6, vignette=0.5, seed=1, tint=None):
    im.convert("RGB").save(path)
    post(path, grain=grain, vignette=vignette, seed=seed, tint=tint)


def oscuro_borroso(path, f=0.35, r=14, zoom=1.0, centro=(960, 540)):
    im = Image.open(path).convert("RGB")
    if zoom != 1.0:
        w, h = im.size
        cw, ch = w / zoom, h / zoom
        x0, y0 = centro[0] - cw / 2, centro[1] - ch / 2
        im = im.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(r))
    return ImageEnhance.Brightness(im).enhance(f)


def font(p, s):
    return ImageFont.truetype(p, s)


# ---------------------------------------------------------------------------

def foto():
    """Foto en blanco y negro de Tomás a los veinte, bajo los pimientos."""
    # escena interior de la foto
    body = ('<rect width="1920" height="1080" fill="#3a4250"/>'
            + pimiento(700, -200, 1500, 1100, 71, base="#1b2a22", hoja="#2a3d31", tronco_y=1100, densidad=1.0)
            + '<rect width="1920" height="1080" fill="#9fb0c0" opacity="0.15"/>')
    render(doc(body), f"{TMP}/foto_bg.png")
    bg = Image.open(f"{TMP}/foto_bg.png").convert("RGBA")
    tj = Image.open(os.path.join(ARTE, "tomas_joven.png")).convert("RGBA")
    tj = tj.resize((int(820 * 1.15), int(1080 * 1.15)), Image.LANCZOS)
    bg.alpha_composite(tj, (int(960 - 410 * 1.15), 1080 - int(1080 * 1.15) + 140))
    inner = bg.crop((560, 60, 1360, 1080)).resize((600, 765), Image.LANCZOS)
    inner = bn(inner)
    inner = ImageEnhance.Contrast(inner).enhance(1.1)
    inner = grano(inner, 14, seed=3)
    inner = vineta(inner, 0.7)
    inner = rayas(inner, 25, seed=4)
    inner = sepia(inner, 0.25)
    # marco de papel fotográfico
    marco = Image.new("RGB", (660, 860), (226, 220, 206))
    marco.paste(inner, (30, 30))
    d = ImageDraw.Draw(marco)
    d.text((330, 818), "Copiapó, 1968", font=font(SERIF_C, 26), fill=(90, 80, 70), anchor="mm")
    marco = marco.filter(ImageFilter.GaussianBlur(0.4))
    # fondo: repisa de madera oscura
    base = Image.new("RGB", (1920, 1080), (26, 18, 13))
    a = np.asarray(base).astype(np.float32)
    rng = np.random.default_rng(5)
    vetas = np.cumsum(rng.normal(0, 1, (1080, 1)), 0) * 0.6 + np.sin(np.linspace(0, 40, 1920))[None, :] * 3
    a += vetas[..., None] * np.array([1.0, 0.7, 0.5])
    base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    sombra = Image.new("RGBA", (720, 920), (0, 0, 0, 0))
    ImageDraw.Draw(sombra).rectangle([30, 30, 690, 890], fill=(0, 0, 0, 170))
    sombra = sombra.filter(ImageFilter.GaussianBlur(18)).rotate(-3, expand=True, resample=Image.BICUBIC)
    m = marco.convert("RGBA").rotate(-3, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    base = base.convert("RGBA")
    base.alpha_composite(sombra, (960 - sombra.width // 2 + 14, 540 - sombra.height // 2 + 20))
    base.alpha_composite(m, (960 - m.width // 2, 540 - m.height // 2))
    # luz de lámpara cálida
    luz = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(luz).ellipse([500, 0, 1700, 1100], fill=(255, 190, 120, 40))
    luz = luz.filter(ImageFilter.GaussianBlur(120))
    base.alpha_composite(luz)
    guardar(base, f"{CG}/foto.png", grain=6, vignette=0.6, seed=21)


def espejo(con_ines):
    fondos.taxi_frente(True)
    base = oscuro_borroso(f"{OUT}/bg/taxi_frente_detenido.png", f=0.32, r=16, zoom=1.6, centro=(960, 300))
    # contenido del espejo: asiento trasero
    asiento = Image.open(f"{OUT}/bg/taxi_atras.png").convert("RGBA").resize((1500, 844), Image.LANCZOS)
    asiento = asiento.transpose(Image.FLIP_LEFT_RIGHT)
    if con_ines:
        ir = Image.open(os.path.join(ARTE, "ines_raw.png")).convert("RGBA")
        cara = ir.crop((180, 70, 640, 560)).resize((920, 980), Image.LANCZOS)
        cara = cara.transpose(Image.FLIP_LEFT_RIGHT)
        # tono frío fantasmal
        r_, g_, b_, a_ = cara.split()
        rgb = Image.merge("RGB", (r_, g_, b_))
        rgb = Image.blend(rgb, ImageOps.colorize(ImageOps.grayscale(rgb), (10, 14, 28), (220, 232, 255)), 0.45)
        cara = Image.merge("RGBA", (*rgb.split(), a_))
        asiento.alpha_composite(cara, (750 - 460, 30))
    asiento = asiento.crop((80, 120, 1420, 600))
    W_, H_ = 1340, 480
    mask = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, W_ - 1, H_ - 1], radius=90, fill=255)
    asiento = ImageEnhance.Brightness(asiento.convert("RGB")).enhance(0.85).filter(ImageFilter.GaussianBlur(1.2))
    asiento = asiento.convert("RGBA")
    asiento.putalpha(mask)
    base = base.convert("RGBA")
    # carcasa del espejo
    carc = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    d = ImageDraw.Draw(carc)
    d.rectangle([940, 0, 980, 230], fill=(14, 14, 16, 255))
    d.rounded_rectangle([290, 200, 1630, 760], radius=120, fill=(12, 12, 15, 255))
    carc_sh = carc.filter(ImageFilter.GaussianBlur(20))
    base.alpha_composite(Image.eval(carc_sh, lambda v: v) , (0, 18))
    base.alpha_composite(carc)
    base.alpha_composite(asiento, (290 + 0, 240))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([290, 240, 1630, 720], radius=90, outline=(58, 62, 70, 255), width=6)
    # reflejo del vidrio
    brillo = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(brillo).polygon([(420, 250), (700, 250), (480, 710), (300, 710)], fill=(255, 255, 255, 18))
    base.alpha_composite(brillo)
    # rosario delante
    d = ImageDraw.Draw(base)
    for i in range(30):
        t = i / 29
        ang = math.pi * t
        x = 1250 + 90 * math.cos(ang)
        y = 720 + 300 * math.sin(ang) * 0.9
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(70, 44, 92, 255))
    d.rectangle([1243, 990, 1257, 1080], fill=(180, 160, 110, 255))
    d.rectangle([1222, 1012, 1278, 1026], fill=(180, 160, 110, 255))
    nombre = "espejo_ines" if con_ines else "espejo_vacio"
    guardar(base, f"{CG}/{nombre}.png", grain=7, vignette=0.6, seed=22, tint=((6, 8, 20), (200, 220, 255)))


def billete():
    base = oscuro_borroso(f"{OUT}/bg/taxi_frente_detenido.png", f=0.28, r=20, zoom=1.3, centro=(960, 800)).convert("RGBA")
    # billete (diseño genérico inventado)
    bw, bh = 900, 420
    bill = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(bill, "RGBA")
    d.rounded_rectangle([0, 0, bw - 1, bh - 1], radius=10, fill=(170, 128, 86, 255))
    rnd = random.Random(8)
    for k in range(0, bw, 6):
        d.line([(k, 0), (k + 40, bh)], fill=(150, 108, 70, 120), width=1)
    d.rectangle([18, 18, bw - 19, bh - 19], outline=(92, 58, 34, 255), width=6)
    d.rectangle([34, 34, bw - 35, bh - 35], outline=(110, 72, 44, 255), width=2)
    for k in range(40):
        x = 34 + k * (bw - 68) / 39
        d.ellipse([x - 5, 26 - 5, x + 5, 26 + 5], outline=(92, 58, 34, 255), width=2)
        d.ellipse([x - 5, bh - 26 - 5, x + 5, bh - 26 + 5], outline=(92, 58, 34, 255), width=2)
    # óvalo con retrato genérico
    d.ellipse([560, 70, 820, 350], fill=(196, 160, 118, 255), outline=(92, 58, 34, 255), width=5)
    d.ellipse([640, 120, 740, 240], fill=(120, 86, 58, 255))
    d.pieslice([590, 220, 790, 420], 180, 360, fill=(120, 86, 58, 255))
    d.text((300, 92), "REPÚBLICA DE CHILE", font=font(SERIF_B, 34), fill=(70, 40, 22, 255), anchor="mm")
    d.text((300, 200), "DIEZ", font=font(SERIF_B, 86), fill=(70, 40, 22, 255), anchor="mm")
    d.text((300, 278), "ESCUDOS", font=font(SERIF_B, 50), fill=(70, 40, 22, 255), anchor="mm")
    d.text((110, 350), "E° 10", font=font(SERIF_B, 40), fill=(70, 40, 22, 255), anchor="mm")
    d.text((440, 350), "A 4 0 2 3 4 7", font=font(SERIF, 26), fill=(120, 30, 30, 255), anchor="mm")
    # arrugas y manchas
    a = np.asarray(bill).astype(np.float32)
    rng = np.random.default_rng(3)
    a[..., :3] *= (0.92 + 0.08 * rng.random((bh, bw, 1)))
    bill = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
    capa = Image.new("RGBA", bill.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.line([(bw * 0.5, 4), (bw * 0.48, bh - 4)], fill=(90, 60, 40, 140), width=4)
    d.line([(4, bh * 0.5), (bw - 4, bh * 0.52)], fill=(90, 60, 40, 100), width=3)
    for _ in range(10):
        r = rnd.uniform(10, 40)
        x, y = rnd.uniform(r + 10, bw - r - 10), rnd.uniform(r + 10, bh - r - 10)
        d.ellipse([x - r, y - r * 0.6, x + r, y + r * 0.6], fill=(90, 60, 30, 40))
    capa = capa.filter(ImageFilter.GaussianBlur(3))
    bill.alpha_composite(capa)
    bill = bill.rotate(8, expand=True, resample=Image.BICUBIC)
    # mano abierta (palma hacia arriba): muñeca abajo, dedos asomando sobre el billete
    svg = ('<g stroke="#16100f" stroke-width="5">'
           '<path d="M700,1080 C690,960 700,860 740,800 L1180,790 C1230,860 1240,960 1230,1080 Z" fill="#b98466"/>'
           + "".join(f'<rect x="{x}" y="{y}" width="92" height="{hgt}" rx="44" fill="#c08c6e" transform="rotate({rot} {x+46} {y+hgt})"/>'
                     for (x, y, hgt, rot) in [(760, 300, 330, -8), (870, 260, 370, -3), (980, 270, 360, 2), (1090, 320, 300, 8)])
           + '<path d="M700,860 C620,800 560,700 600,640 C630,600 690,640 720,700 L760,780 Z" fill="#b07a5e"/>'
           '</g>'
           '<path d="M760,840 C880,820 1040,820 1180,840" stroke="#8a5a46" stroke-width="5" fill="none" opacity="0.6"/>')
    render(doc(svg), f"{TMP}/mano.png")
    mano = Image.open(f"{TMP}/mano.png").convert("RGBA")
    base.alpha_composite(mano)
    sh = Image.new("RGBA", bill.size, (0, 0, 0, 0))
    sh.putalpha(bill.split()[3].point(lambda v: int(v * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(sh, (960 - bill.width // 2 + 20, 560 - bill.height // 2 + 30))
    base.alpha_composite(bill, (960 - bill.width // 2, 560 - bill.height // 2))
    luz = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(luz).polygon([(0, 300), (1920, 120), (1920, 420), (0, 700)], fill=(255, 170, 90, 38))
    base.alpha_composite(luz.filter(ImageFilter.GaussianBlur(40)))
    guardar(base, f"{CG}/billete.png", grain=7, vignette=0.65, seed=23, tint=((8, 6, 14), (255, 190, 130)))


def chaqueta_asiento():
    base = oscuro_borroso(f"{OUT}/bg/taxi_atras.png", f=0.75, r=3).convert("RGBA")
    defs = sprites.tejido_pattern("lanaC", sprites.ROJO, sprites.ROJO_S, paso=12)
    svg = ('<g>'
           # sombra
           '<ellipse cx="960" cy="900" rx="560" ry="70" fill="#000" opacity="0.6" filter="url(#b16)"/>'
           # cuerpo doblado
           '<path d="M470,880 C460,760 480,690 560,660 L1360,640 C1440,650 1470,720 1460,880 Z" fill="url(#lanaC)" stroke="#16100f" stroke-width="5"/>'
           '<path d="M470,880 C470,850 1460,840 1460,880 L1460,900 L470,900 Z" fill="#5c0c1a" stroke="#16100f" stroke-width="4"/>'
           # manga doblada cruzando
           '<path d="M520,700 C700,740 900,760 1180,720 L1200,780 C900,830 700,810 510,770 Z" fill="#8f1527" stroke="#16100f" stroke-width="4"/>'
           '<path d="M1180,720 C1240,710 1280,730 1290,760 L1200,780 Z" fill="#5c0c1a" stroke="#16100f" stroke-width="4"/>'
           # cuello chal y solapa
           '<path d="M700,660 C760,600 1150,590 1220,650 C1150,640 760,650 700,690 Z" fill="#5c0c1a" stroke="#16100f" stroke-width="4"/>'
           '<path d="M760,664 L900,820 L940,820 L820,660 Z" fill="#6e0f20" stroke="#16100f" stroke-width="3"/>'
           # sobre en el bolsillo interior
           '<g transform="rotate(-6 1010 690)"><rect x="900" y="640" width="250" height="140" fill="#e7dcc2" stroke="#4a3f30" stroke-width="3"/>'
           '<path d="M900,640 L1025,720 L1150,640" stroke="#b8aa8c" stroke-width="3" fill="none"/></g>'
           '<path d="M860,690 C980,700 1100,700 1240,680 L1250,760 C1100,780 980,780 860,770 Z" fill="#8f1527" stroke="#16100f" stroke-width="4"/>'
           # botones
           '<circle cx="1330" cy="790" r="16" fill="#3a2418" stroke="#16100f" stroke-width="3"/><circle cx="1180" cy="820" r="16" fill="#3a2418" stroke="#16100f" stroke-width="3"/>'
           '</g>'
           + sprites.paloma(800, 700, 1.4)
           + '<text x="1010" y="672" font-family="DejaVu Serif" font-style="italic" font-size="34" fill="#3a2a1a" text-anchor="middle" transform="rotate(-6 1010 690)">Para Tomás</text>'
           # luz de farol cruzando
           '<path d="M0,620 L1920,470 L1920,600 L0,760 Z" fill="#f2a65a" opacity="0.16" filter="url(#b16)"/>'
           '<circle cx="800" cy="700" r="60" fill="#ffffff" opacity="0.12" filter="url(#b16)"/>')
    svg = '<g transform="translate(960 760) scale(1.35) translate(-960 -760)">' + svg + '</g>'
    render(doc(svg, defs), f"{TMP}/chaq.png")
    base.alpha_composite(Image.open(f"{TMP}/chaq.png").convert("RGBA"))
    guardar(base, f"{CG}/chaqueta_asiento.png", grain=7, vignette=0.7, seed=24, tint=((8, 6, 16), (255, 180, 120)))


def libro():
    rnd = random.Random(30)
    W_, H_ = 1920, 1080
    base = Image.new("RGB", (W_, H_), (20, 14, 10))
    a = np.asarray(base).astype(np.float32)
    rng = np.random.default_rng(31)
    a += (np.cumsum(rng.normal(0, 1, (H_, 1)), 0) * 0.5 + np.sin(np.linspace(0, 60, W_))[None, :] * 2)[..., None] * np.array([1, 0.7, 0.5])
    base = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    pag = Image.new("RGBA", (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(pag)
    # cuaderno abierto
    d.polygon([(240, 170), (950, 140), (960, 960), (220, 990)], fill=(214, 202, 172, 255))
    d.polygon([(970, 140), (1690, 170), (1710, 990), (960, 960)], fill=(222, 210, 182, 255))
    d.line([(960, 140), (960, 960)], fill=(140, 120, 90, 255), width=4)
    for k in range(24):
        y = 230 + k * 30
        d.line([(250, y + (950 - 250) * -0.04 * 0), (945, y - 26)], fill=(160, 170, 190, 110), width=1)
        d.line([(975, y - 26), (1695, y)], fill=(160, 170, 190, 110), width=1)
    d.line([(300, 170), (290, 985)], fill=(200, 90, 90, 120), width=2)
    nombres = ["L. Carvajal. Trajo la chaqueta.", "M. Araya", "H. Rojas", "J. Tapia", "O. Cerda", "R. Godoy", "E. Vallejos",
               "S. Muñoz", "A. Contreras", "G. Ramírez", "F. Olivares", "N. Bugueño", "C. Pastén", "V. Toro", "J. Castillo",
               "P. Ahumada", "L. Rivera", "D. Ossandón", "T. Herrera", "M. Bravo", "R. Peña", "I. Alfaro"]
    fuente = font(SERIF_C, 23)
    for i, nm in enumerate(nombres):
        y = 228 + i * 30
        anio = 1969 + i
        txt = f"8 nov. {anio} — {nm}"
        col = (40, 34, 60, 255) if i else (30, 24, 44, 255)
        d.text((310, y - 22 - i * 1.0), txt, font=fuente, fill=col)
    nombres2 = ["G. Rojas", "B. Salinas", "K. Aracena", "E. Cortés", "Mirta S. (Los Carrera)", "J. Villalobos",
                "C. Flores", "M. Araya (otra vez)", "A. Pinto", "F. Iturra", "R. Moyano", "Mirta S. (otra vez)",
                "H. Barraza", "Y. Cáceres", "D. Campillay", "Pato Cortés", "W. Saavedra", "L. Rojo", "S. Guerra",
                "E. Rivera", "N. Plaza", "Mirta S."]
    for i, nm in enumerate(nombres2):
        y = 228 + i * 30
        anio = 2004 + i
        d.text((995, y - 24 + i * 1.0), f"8 nov. {anio} — {nm}", font=fuente, fill=(28, 34, 70, 255))
    d.text((995, 228 + 22 * 30 - 2), "8 nov. 2026 —", font=fuente, fill=(28, 34, 70, 120))
    pag = pag.filter(ImageFilter.GaussianBlur(0.5))
    base.alpha_composite(pag)
    # haz de linterna
    luz = Image.new("L", (W_, H_), 0)
    ImageDraw.Draw(luz).ellipse([180, 60, 1560, 1020], fill=255)
    luz = luz.filter(ImageFilter.GaussianBlur(120))
    oscuro = Image.new("RGBA", (W_, H_), (0, 0, 0, 255))
    oscuro.putalpha(luz.point(lambda v: int(200 - v * 0.78)))
    base.alpha_composite(oscuro)
    calido = Image.new("RGBA", (W_, H_), (255, 230, 170, 0))
    calido.putalpha(luz.point(lambda v: int(v * 0.12)))
    base.alpha_composite(calido)
    guardar(base, f"{CG}/libro.png", grain=6, vignette=0.6, seed=25)


def ovalo_ines(w, h):
    ir = Image.open(os.path.join(ARTE, "ines_raw.png")).convert("RGBA")
    cara = ir.crop((230, 90, 590, 560))
    fondo = Image.new("RGBA", cara.size, (190, 178, 160, 255))
    fondo.alpha_composite(cara)
    fondo = sepia(fondo).resize((w, h), Image.LANCZOS)
    fondo = vineta(fondo, 0.8)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, w - 1, h - 1], fill=255)
    out = fondo.convert("RGBA")
    out.putalpha(mask)
    return out


def placa(d, x, y, w, h, lineas, num, foto_img=None, base_img=None, paloma_svg=False):
    base_im = d._image
    d.rectangle([x - 14, y - 14, x + w + 14, y + h + 14], fill=(70, 66, 62, 255))
    d.rectangle([x, y, x + w, y + h], fill=(206, 202, 194, 255))
    capa = Image.new("RGBA", base_im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    for k in range(14):
        xx = x + random.uniform(0, w)
        d.line([(xx, y), (xx + random.uniform(-120, 120), y + h)], fill=(150, 146, 140, 40), width=2)
    d.text((x + w - 20, y + 30), str(num), font=font(SERIF, 26), fill=(80, 76, 70, 255), anchor="rm")
    yy = y + (h * 0.56 if foto_img else h * 0.3)
    for (txt, f, sz) in lineas:
        d.text((x + w / 2 + 2, yy + 2), txt, font=font(f, sz), fill=(250, 250, 250, 150), anchor="mm")
        d.text((x + w / 2, yy), txt, font=font(f, sz), fill=(38, 36, 34, 255), anchor="mm")
        yy += sz * 1.6
    base_im.alpha_composite(capa)


def nicho():
    random.seed(40)
    base = Image.new("RGBA", (1920, 1080), (14, 14, 18, 255))
    d = ImageDraw.Draw(base)
    # nichos vecinos
    for (x, y) in [(-500, -380), (560, -380), (1620, -380), (-500, 820), (1620, 820), (560, 820), (-500, 220), (1620, 220)]:
        placa(d, x, y, 780, 500, [("· · ·", SERIF, 30)], "")
    x, y, w, h = 560, 220, 800, 560
    placa(d, x, y, w, h, [("INÉS ALBORNOZ VEGA", SERIF_B, 46), ("3 · V · 1950   —   8 · XI · 1968", SERIF, 32),
                          ("TUS PADRES NO TE OLVIDAN", SERIF_I, 28)], 2347, foto_img=True)
    ov = ovalo_ines(170, 220)
    marco = Image.new("RGBA", (196, 246), (0, 0, 0, 0))
    ImageDraw.Draw(marco).ellipse([0, 0, 195, 245], fill=(170, 140, 80, 255))
    base.alpha_composite(marco, (960 - 98, 248))
    base.alpha_composite(ov, (960 - 85, 261))
    # flores de plástico y vela
    flores = ('<g>'
              '<rect x="640" y="760" width="90" height="120" rx="8" fill="#cfe0e4" opacity="0.4"/>'
              '<ellipse cx="685" cy="740" rx="9" ry="18" fill="#fff0c0"/><circle cx="685" cy="745" r="110" fill="url(#glowVela)"/>'
              + "".join(f'<path d="M{1150 + k*18},{880} Q{1140 + k*22},{800} {1130 + k*30},{740 - (k%3)*20}" stroke="#4a6a3a" stroke-width="5" fill="none"/>'
                        f'<circle cx="{1130 + k*30}" cy="{740 - (k%3)*20}" r="22" fill="{["#b84a6a","#d8c060","#c87a9a","#e8e0e0","#9a5ab0"][k%5]}" opacity="0.75"/>' for k in range(6))
              + '</g>')
    render(doc(flores), f"{TMP}/flores.png")
    base.alpha_composite(Image.open(f"{TMP}/flores.png").convert("RGBA"))
    # linterna
    luz = Image.new("L", (1920, 1080), 0)
    ImageDraw.Draw(luz).ellipse([400, 80, 1560, 1000], fill=255)
    luz = luz.filter(ImageFilter.GaussianBlur(110))
    osc = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
    osc.putalpha(luz.point(lambda v: int(225 - v * 0.85)))
    base.alpha_composite(osc)
    fr = Image.new("RGBA", (1920, 1080), (190, 210, 255, 0))
    fr.putalpha(luz.point(lambda v: int(v * 0.08)))
    base.alpha_composite(fr)
    guardar(base, f"{CG}/nicho.png", grain=7, vignette=0.6, seed=26, tint=((6, 8, 20), (255, 230, 190)))


def ticket(nombre, asiento):
    tw, th = 820, 340
    t = Image.new("RGBA", (tw, th), (232, 224, 200, 255))
    d = ImageDraw.Draw(t)
    d.rectangle([0, 0, tw, 70], fill=(150, 34, 40, 255))
    d.text((tw / 2, 36), "ESTRELLA DEL NORTE", font=font(SERIF_B, 40), fill=(245, 236, 214, 255), anchor="mm")
    d.text((30, 110), "COPIAPÓ — LA SERENA", font=font(SERIF_B, 34), fill=(40, 40, 60, 255))
    d.text((30, 160), "Sábado 9 de noviembre de 1968", font=font(SERIF, 28), fill=(40, 40, 60, 255))
    d.text((30, 205), "Salida: 00:15     Asiento: " + asiento, font=font(SERIF, 28), fill=(40, 40, 60, 255))
    d.text((30, 262), "Pasajero: " + nombre, font=font(SERIF_C, 28), fill=(30, 30, 90, 255))
    d.line([(620, 80), (620, th)], fill=(120, 110, 90, 255), width=2)
    for yy in range(80, th, 16):
        d.ellipse([614, yy, 626, yy + 8], fill=(120, 110, 90, 255))
    d.text((720, 150), "E° 18", font=font(SERIF_B, 40), fill=(150, 34, 40, 255), anchor="mm")
    d.text((720, 230), "Nº 0" + asiento + "47", font=font(SERIF, 24), fill=(60, 60, 60, 255), anchor="mm")
    a = np.asarray(t).astype(np.float32)
    rng = np.random.default_rng(len(nombre))
    a[..., :3] *= (0.9 + 0.1 * rng.random((th, tw, 1)))
    t = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA")
    d = ImageDraw.Draw(t)
    d.line([(tw * 0.45, 0), (tw * 0.47, th)], fill=(150, 130, 100, 120), width=3)
    return t


def pasajes():
    defs = sprites.tejido_pattern("lanaP", sprites.ROJO, sprites.ROJO_S, paso=22)
    render(doc('<rect width="1920" height="1080" fill="url(#lanaP)"/>', defs), f"{TMP}/lana.png")
    base = Image.open(f"{TMP}/lana.png").convert("RGB")
    base = ImageEnhance.Brightness(base).enhance(0.55).filter(ImageFilter.GaussianBlur(1)).convert("RGBA")
    # sobre abierto y carta doblada
    d = ImageDraw.Draw(base)
    d.polygon([(1240, 620), (1800, 580), (1840, 980), (1280, 1020)], fill=(214, 200, 168, 255))
    d.polygon([(1240, 620), (1540, 760), (1800, 580)], fill=(196, 182, 150, 255))
    for i, (nm, a_, pos, ang) in enumerate([("I. Albornoz V.", "14", (120, 90), 5), ("T. Pizarro L.", "15", (620, 480), -4)]):
        tk = ticket(nm, a_).rotate(ang, expand=True, resample=Image.BICUBIC)
        sh = Image.new("RGBA", tk.size, (0, 0, 0, 0))
        sh.putalpha(tk.split()[3].point(lambda v: int(v * 0.7)))
        base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(16)), (pos[0] + 18, pos[1] + 24))
        base.alpha_composite(tk, pos)
    luz = Image.new("L", (1920, 1080), 0)
    ImageDraw.Draw(luz).ellipse([150, 60, 1500, 1040], fill=255)
    luz = luz.filter(ImageFilter.GaussianBlur(130))
    osc = Image.new("RGBA", (1920, 1080), (0, 0, 0, 255))
    osc.putalpha(luz.point(lambda v: int(190 - v * 0.74)))
    base.alpha_composite(osc)
    guardar(base, f"{CG}/pasajes.png", grain=6, vignette=0.55, seed=27, tint=((10, 6, 10), (255, 225, 180)))


def recuerdo():
    fondos.plaza_noche(path=f"{TMP}/plaza_raw.png", sin_post=True)
    base = Image.open(f"{TMP}/plaza_raw.png").convert("RGBA")
    sprites.tomas_joven(f"{TMP}/tomas_joven_sin.png", chaqueta=False)
    tj = Image.open(f"{TMP}/tomas_joven_sin.png").convert("RGBA")
    ir = Image.open(os.path.join(ARTE, "ines_raw_sonrisa.png")).convert("RGBA")
    s = 0.92
    tj = tj.resize((int(820 * s), int(1080 * s)), Image.LANCZOS)
    ir = ir.resize((int(820 * s * 0.95), int(1080 * s * 0.95)), Image.LANCZOS)
    base.alpha_composite(tj, (560, 1080 - tj.height + 30))
    base.alpha_composite(ir, (980, 1080 - ir.height + 40))
    im = sepia(base.convert("RGB"))
    im = ImageEnhance.Brightness(im).enhance(1.35)
    im = ImageEnhance.Contrast(im).enhance(0.9)
    im = grano(im, 12, seed=8)
    im = rayas(im, 60, seed=9)
    # bordes desenfocados de recuerdo
    blur = im.filter(ImageFilter.GaussianBlur(10))
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([200, 60, 1720, 1100], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(90))
    im = Image.composite(im, blur, mask)
    im = vineta(im, 0.75)
    d = ImageDraw.Draw(im)
    d.text((1840, 1040), "1968", font=font(SERIF_C, 40), fill=(230, 210, 170), anchor="rm")
    guardar(im, f"{CG}/recuerdo.png", grain=5, vignette=0.3, seed=28)


def carta():
    fondos.casa_noche()
    base = oscuro_borroso(f"{OUT}/bg/casa_noche.png", f=0.35, r=18).convert("RGBA")
    svg = ('<g transform="rotate(-2 960 540)">'
           '<rect x="520" y="70" width="880" height="1000" fill="#000" opacity="0.5" filter="url(#b16)" transform="translate(16,20)"/>'
           '<rect x="520" y="70" width="880" height="1000" fill="#e9e0c8"/>'
           '<line x1="520" y1="320" x2="1400" y2="322" stroke="#c9bd9e" stroke-width="3"/>'
           '<line x1="520" y1="570" x2="1400" y2="572" stroke="#c9bd9e" stroke-width="3"/>'
           '<line x1="520" y1="820" x2="1400" y2="822" stroke="#c9bd9e" stroke-width="3"/>'
           + texto(600, 170, "Tomás:", 48, fill="#24305a", style="italic", anchor="start")
           + garabatos(600, 240, 720, 18, 40, 77, color="#24305a", sw=2.4, op=0.8)
           + texto(1240, 1010, "Inés", 52, fill="#24305a", style="italic", anchor="middle")
           + '</g>'
           # manos viejas en los bordes
           '<path d="M420,1080 C430,1010 470,980 520,990 L560,1080 Z" fill="#b8957e" stroke="#16100f" stroke-width="5"/>'
           '<path d="M500,1080 C500,1010 530,950 575,930 C605,918 625,940 612,968 C596,1000 585,1040 590,1080 Z" fill="#cfae96" stroke="#16100f" stroke-width="5"/>'
           '<path d="M572,944 C584,934 600,936 604,948" stroke="#8a6a5a" stroke-width="3" fill="#e2c8b6"/>'
           '<path d="M1500,1080 C1490,1010 1450,980 1400,990 L1360,1080 Z" fill="#a8856e" stroke="#16100f" stroke-width="5"/>'
           '<path d="M1420,1080 C1420,1010 1390,950 1345,930 C1315,918 1295,940 1308,968 C1324,1000 1335,1040 1330,1080 Z" fill="#b8957e" stroke="#16100f" stroke-width="5"/>'
           '<path d="M1348,944 C1336,934 1320,936 1316,948" stroke="#8a6a5a" stroke-width="3" fill="#d2b6a2"/>'
           '<ellipse cx="960" cy="400" rx="700" ry="500" fill="#ffd08a" opacity="0.10" filter="url(#b60)"/>')
    render(doc(svg), f"{TMP}/carta.png")
    base.alpha_composite(Image.open(f"{TMP}/carta.png").convert("RGBA"))
    guardar(base, f"{CG}/carta.png", grain=6, vignette=0.6, seed=29, tint=((10, 8, 16), (255, 210, 160)))


def nichos_final():
    random.seed(50)
    base = Image.new("RGBA", (1920, 1080), (120, 104, 96, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in [(-420, -360), (590, -360), (1420, -360), (-420, 860), (590, 860), (1420, 860)]:
        placa(d, x, y, 740, 480, [("· · ·", SERIF, 30)], "")
    placa(d, 100, 230, 760, 560, [("INÉS ALBORNOZ VEGA", SERIF_B, 42), ("1950  —  1968", SERIF, 34),
                                  ("TUS PADRES NO TE OLVIDAN", SERIF_I, 26)], 2347, foto_img=True)
    placa(d, 1060, 230, 760, 560, [("TOMÁS PIZARRO LEIVA", SERIF_B, 42), ("1948  —  2027", SERIF, 34),
                                   ("LLEGASTE.", SERIF_I, 30)], 2348, foto_img=True)
    ov = ovalo_ines(150, 196)
    m = Image.new("RGBA", (174, 220), (0, 0, 0, 0))
    ImageDraw.Draw(m).ellipse([0, 0, 173, 219], fill=(170, 140, 80, 255))
    base.alpha_composite(m, (480 - 87, 250))
    base.alpha_composite(ov, (480 - 75, 262))
    # palomita grabada en la placa de Tomás
    render(doc(sprites.paloma(960, 540, 3.2, color="#bdb8b0", sombra="#5f5a54")), f"{TMP}/paloma.png")
    pal = Image.open(f"{TMP}/paloma.png").convert("RGBA").crop((780, 420, 1140, 640))
    base.alpha_composite(pal, (1440 - 180, 270))
    # frasco con nardos
    nardos = ['<g>', '<rect x="900" y="700" width="120" height="200" rx="14" fill="#d8eef0" opacity="0.55" stroke="#8aa" stroke-width="3"/>']
    rnd = random.Random(51)
    for k in range(7):
        x0 = 930 + k * 10
        x1 = 860 + k * 33 + rnd.uniform(-10, 10)
        y1 = 380 + rnd.uniform(-40, 40)
        nardos.append(f'<path d="M{x0},{880} Q{(x0+x1)/2},{600} {x1:.0f},{y1:.0f}" stroke="#4a6a3a" stroke-width="5" fill="none"/>')
        for j in range(9):
            t = j / 8
            xx = x1 + (x0 - x1) * t * 0.35
            yy = y1 + (880 - y1) * t * 0.35
            nardos.append(f'<ellipse cx="{xx + rnd.uniform(-10,10):.0f}" cy="{yy:.0f}" rx="12" ry="9" fill="#f6f2ea" stroke="#c9c2b2" stroke-width="2"/>')
    nardos.append('</g>')
    render(doc("".join(nardos)), f"{TMP}/nardos.png")
    base.alpha_composite(Image.open(f"{TMP}/nardos.png").convert("RGBA"))
    # luz de mañana
    luz = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
    ImageDraw.Draw(luz).polygon([(0, 0), (900, 0), (1920, 900), (1920, 1080), (1200, 1080)], fill=(255, 210, 150, 60))
    base.alpha_composite(luz.filter(ImageFilter.GaussianBlur(60)))
    guardar(base, f"{CG}/nichos_final.png", grain=5, vignette=0.55, seed=30, tint=((40, 24, 30), (255, 220, 170)))


def escena_titulo(path, con_texto=True, para_menu=False):
    d1, sky = fondos.cielo(y_bot=760)
    b = [sky, via_lactea(1300, 150, 800, 160, -16, 61), estrellas(700, 62, y_max=640),
         cerro(660, 250, 63, "#0c1320", rim="#3a5170"), cerro(720, 150, 64, "#080c13")]
    b.append(f'<rect y="740" width="1920" height="340" fill="#0c0f14"/>')
    b.append(farol(1500, 900, 520, escala=1.2))
    b.append('<ellipse cx="1200" cy="900" rx="600" ry="120" fill="url(#pozoSodio)"/>')
    # banca de frente con la chaqueta
    bx, by = 980, 760
    b.append(f'<rect x="{bx}" y="{by}" width="520" height="24" fill="#0a0c0f"/>')
    b.append(f'<rect x="{bx}" y="{by+40}" width="520" height="22" fill="#0a0c0f"/>')
    b.append(f'<rect x="{bx}" y="{by+92}" width="520" height="22" fill="#14171c"/>')
    b.append(f'<rect x="{bx+20}" y="{by+110}" width="18" height="120" fill="#0a0c0f"/><rect x="{bx+482}" y="{by+110}" width="18" height="120" fill="#0a0c0f"/>')
    b.append(f'<rect x="{bx}" y="{by+92}" width="520" height="4" fill="#f2a65a" opacity="0.7"/>')
    defs = d1 + sprites.tejido_pattern("lanaT", sprites.ROJO, sprites.ROJO_S, paso=10)
    # chaqueta doblada sobre el asiento, con una manga cayendo
    b.append(f'<path d="M{bx+110},{by+92} C{bx+100},{by+40} {bx+130},{by+10} {bx+190},{by+4} L{bx+380},{by} C{bx+430},{by+6} {bx+450},{by+50} {bx+440},{by+92} Z" fill="url(#lanaT)" stroke="#16100f" stroke-width="4"/>')
    b.append(f'<path d="M{bx+180},{by+8} C{bx+230},{by+50} {bx+300},{by+50} {bx+350},{by+4}" fill="#5c0c1a" stroke="#16100f" stroke-width="3"/>')
    b.append(f'<path d="M{bx+400},{by+60} C{bx+430},{by+90} {bx+440},{by+150} {bx+430},{by+230} L{bx+392},{by+232} C{bx+398},{by+160} {bx+390},{by+110} {bx+370},{by+92} Z" fill="url(#lanaT)" stroke="#16100f" stroke-width="4"/>')
    b.append(f'<path d="M{bx+392},{by+214} L{bx+432},{by+212}" stroke="#5c0c1a" stroke-width="10"/>')
    b.append(sprites.paloma(bx + 240, by + 46, 0.7))
    b.append(f'<path d="M{bx+440},{by+20} L{bx+444},{by+90}" stroke="#f2a65a" stroke-width="4" opacity="0.5"/>')
    # pimiento sobre la banca
    b.append(pimiento(1150, -180, 1300, 980, 65, base="#0a120f", hoja="#14211a", luz="#2e2b19", tronco_y=820, densidad=1.2, luz_x=1500))
    b.append(pimiento(-100, -300, 800, 820, 66, base="#050907", hoja="#0b140e", tronco_y=-200, densidad=0.8))
    if para_menu:
        b.append('<rect width="640" height="1080" fill="#000" opacity="0.35"/>')
    if con_texto:
        b.append('<rect x="0" y="380" width="1920" height="300" fill="#000" opacity="0.25" filter="url(#b60)"/>')
        b.append(texto(640, 500, "LA CHAQUETA", 124, fill="#efe7da", weight="bold", spacing=14))
        b.append(texto(640, 580, "Una leyenda de Copiapó", 46, fill="#d9a6a6", style="italic", spacing=3))
        b.append('<rect x="330" y="612" width="620" height="3" fill="#a3192d"/>')
    render(doc("".join(b), defs), path)
    post(path, grain=7, vignette=0.6, tint=((6, 12, 28), (255, 190, 120)), seed=31)


def titulo():
    escena_titulo(f"{CG}/titulo.png", con_texto=True)


def menus():
    escena_titulo(f"{GUI}/main_menu.png", con_texto=False, para_menu=True)
    im = Image.open(f"{GUI}/main_menu.png").filter(ImageFilter.GaussianBlur(14))
    im = ImageEnhance.Brightness(im).enhance(0.45)
    im.save(f"{GUI}/game_menu.png")


TODOS = ["foto", "espejo_v", "espejo_i", "billete", "chaqueta_asiento", "libro", "nicho", "pasajes", "recuerdo", "carta",
         "nichos_final", "titulo", "menus"]

if __name__ == "__main__":
    nombres = sys.argv[1:] or TODOS
    for n in nombres:
        if n == "espejo_v":
            espejo(False)
        elif n == "espejo_i":
            espejo(True)
        else:
            globals()[n]()
        print("ok", n)
