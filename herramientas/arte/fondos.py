"""Fondos de LA CHAQUETA."""
import math
import random
import sys

from lib import *

BG = OUT + "/bg"


def cielo(top="#02040a", mid="#0a1424", bot="#16243a", y_bot=700, gid="cielo"):
    defs = (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{top}"/><stop offset="0.6" stop-color="{mid}"/><stop offset="1" stop-color="{bot}"/></linearGradient>')
    return defs, f'<rect width="{W}" height="{y_bot}" fill="url(#{gid})"/>'


def edificios(y_base, seed, color="#070a10", ventanas=True, x0=0, x1=W, hmin=40, hmax=130):
    rnd = random.Random(seed)
    out = []
    x = x0
    while x < x1:
        bw = rnd.uniform(70, 190)
        bh = rnd.uniform(hmin, hmax)
        out.append(f'<rect x="{x:.0f}" y="{y_base-bh:.0f}" width="{bw+1:.0f}" height="{bh+40:.0f}" fill="{color}"/>')
        if rnd.random() < 0.3:
            out.append(f'<path d="M{x:.0f},{y_base-bh:.0f} L{x+bw/2:.0f},{y_base-bh-rnd.uniform(15,35):.0f} L{x+bw:.0f},{y_base-bh:.0f} Z" fill="{color}"/>')
        if ventanas:
            for _ in range(rnd.randint(0, 3)):
                wx = x + rnd.uniform(8, bw - 22)
                wy = y_base - bh + rnd.uniform(10, bh - 20)
                col = rnd.choice(["#f2b766", "#e9a24f", "#ffd89a", "#9ab7d6"])
                out.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="12" height="16" fill="{col}" opacity="{rnd.uniform(0.5,0.95):.2f}"/>')
        x += bw
    return "".join(out)


def catedral(x, y_base, esc=1.0, color="#080b12", luz="#1a2433"):
    s = esc
    o = []
    # nave
    o.append(f'<rect x="{x-150*s}" y="{y_base-120*s}" width="{300*s}" height="{140*s}" fill="{color}"/>')
    o.append(f'<path d="M{x-160*s},{y_base-120*s} L{x},{y_base-190*s} L{x+160*s},{y_base-120*s} Z" fill="{color}"/>')
    # torre en tres cuerpos
    o.append(f'<rect x="{x-48*s}" y="{y_base-300*s}" width="{96*s}" height="{300*s}" fill="{color}"/>')
    o.append(f'<rect x="{x-38*s}" y="{y_base-380*s}" width="{76*s}" height="{82*s}" fill="{color}"/>')
    o.append(f'<rect x="{x-28*s}" y="{y_base-440*s}" width="{56*s}" height="{62*s}" fill="{color}"/>')
    o.append(f'<path d="M{x-30*s},{y_base-440*s} L{x},{y_base-560*s} L{x+30*s},{y_base-440*s} Z" fill="{color}"/>')
    o.append(f'<rect x="{x-2*s}" y="{y_base-600*s}" width="{4*s}" height="{44*s}" fill="{color}"/>')
    o.append(f'<rect x="{x-14*s}" y="{y_base-588*s}" width="{28*s}" height="{4*s}" fill="{color}"/>')
    # ventanas de campanario (arcos)
    for (yy, ww) in [(y_base - 360 * s, 18 * s), (y_base - 425 * s, 12 * s)]:
        o.append(f'<path d="M{x-ww/2},{yy+24*s} L{x-ww/2},{yy} A{ww/2},{ww/2} 0 0 1 {x+ww/2},{yy} L{x+ww/2},{yy+24*s} Z" fill="{luz}"/>')
    # reloj
    o.append(f'<circle cx="{x}" cy="{y_base-250*s}" r="{18*s}" fill="#c9b78f" opacity="0.55"/>')
    # borde de luna
    o.append(f'<rect x="{x-48*s}" y="{y_base-300*s}" width="{3*s}" height="{300*s}" fill="#3c5878" opacity="0.6"/>')
    return "".join(o)


def estatua_mineria(x, yb, esc=1.0):
    """Fuente con figura femenina de mármol (estilizada)."""
    s = esc
    o = []
    # taza de la fuente
    o.append(f'<ellipse cx="{x}" cy="{yb}" rx="{240*s}" ry="{46*s}" fill="#0e131b"/>')
    o.append(f'<ellipse cx="{x}" cy="{yb-12*s}" rx="{232*s}" ry="{38*s}" fill="#26303e"/>')
    o.append(f'<ellipse cx="{x}" cy="{yb-10*s}" rx="{214*s}" ry="{30*s}" fill="#0a0f16"/>')
    o.append(f'<ellipse cx="{x-60*s}" cy="{yb-10*s}" rx="{70*s}" ry="{6*s}" fill="#7ea3c4" opacity="0.25"/>')
    # pedestal
    o.append(f'<path d="M{x-50*s},{yb-14*s} L{x-38*s},{yb-150*s} L{x+38*s},{yb-150*s} L{x+50*s},{yb-14*s} Z" fill="#cfd7df"/>')
    o.append(f'<path d="M{x+5*s},{yb-14*s} L{x+10*s},{yb-150*s} L{x+38*s},{yb-150*s} L{x+50*s},{yb-14*s} Z" fill="#7f90a4"/>')
    o.append(f'<rect x="{x-58*s}" y="{yb-168*s}" width="{116*s}" height="{20*s}" fill="#dfe6ec"/>')
    o.append(f'<rect x="{x+10*s}" y="{yb-168*s}" width="{48*s}" height="{20*s}" fill="#8696a8"/>')
    # figura con túnica, brazo en alto sosteniendo una lámpara de minero
    fy = yb - 168 * s
    o.append(f'<path d="M{x-40*s},{fy} C{x-36*s},{fy-90*s} {x-30*s},{fy-150*s} {x-18*s},{fy-200*s} '
             f'L{x+16*s},{fy-200*s} C{x+30*s},{fy-150*s} {x+38*s},{fy-90*s} {x+44*s},{fy} Z" fill="#c3ccd5"/>')
    o.append(f'<path d="M{x+2*s},{fy} C{x+6*s},{fy-90*s} {x+10*s},{fy-150*s} {x+6*s},{fy-200*s} '
             f'L{x+16*s},{fy-200*s} C{x+30*s},{fy-150*s} {x+38*s},{fy-90*s} {x+44*s},{fy} Z" fill="#8a9bb0"/>')
    # pliegues
    for k in range(4):
        xx = x - 26 * s + k * 15 * s
        o.append(f'<path d="M{xx},{fy} Q{xx+4*s},{fy-80*s} {xx+2*s},{fy-160*s}" stroke="#9aa9bb" stroke-width="{2*s}" fill="none" opacity="0.7"/>')
    # torso, cabeza
    o.append(f'<path d="M{x-18*s},{fy-200*s} L{x-14*s},{fy-250*s} L{x+14*s},{fy-250*s} L{x+16*s},{fy-200*s} Z" fill="#e8edf1"/>')
    o.append(f'<circle cx="{x}" cy="{fy-266*s}" r="{15*s}" fill="#eef2f5"/>')
    o.append(f'<path d="M{x+2*s},{fy-281*s} A{15*s},{15*s} 0 0 1 {x+2*s},{fy-251*s} Z" fill="#8a9bb0"/>')
    # brazo en alto
    o.append(f'<path d="M{x+10*s},{fy-245*s} L{x+34*s},{fy-300*s} L{x+44*s},{fy-296*s} L{x+20*s},{fy-238*s} Z" fill="#dfe6ec"/>')
    o.append(f'<rect x="{x+30*s}" y="{fy-326*s}" width="{18*s}" height="{24*s}" rx="{3*s}" fill="#e8edf1"/>')
    # brazo bajo
    o.append(f'<path d="M{x-14*s},{fy-245*s} L{x-30*s},{fy-190*s} L{x-22*s},{fy-186*s} L{x-6*s},{fy-238*s} Z" fill="#cfd7df"/>')
    # halo de luz sobre el mármol
    o.append(f'<ellipse cx="{x}" cy="{fy-160*s}" rx="{120*s}" ry="{200*s}" fill="#b8d3ec" opacity="0.10" filter="url(#b30)"/>')
    return "".join(o)


def banca(x, y, esc=1.0, color="#0b0d10", luz=None):
    s = esc
    o = [f'<rect x="{x}" y="{y}" width="{220*s}" height="{10*s}" fill="{color}"/>',
         f'<rect x="{x}" y="{y+16*s}" width="{220*s}" height="{10*s}" fill="{color}"/>',
         f'<rect x="{x}" y="{y-34*s}" width="{220*s}" height="{8*s}" fill="{color}"/>',
         f'<rect x="{x}" y="{y-20*s}" width="{220*s}" height="{8*s}" fill="{color}"/>',
         f'<path d="M{x+14*s},{y-40*s} l{-6*s},{110*s} M{x+206*s},{y-40*s} l{6*s},{110*s}" stroke="{color}" stroke-width="{7*s}"/>']
    if luz:
        o.append(f'<rect x="{x}" y="{y}" width="{220*s}" height="{3*s}" fill="{luz}" opacity="0.6"/>')
    return "".join(o)


def taxi_chileno(x, y, esc=1.0, flip=False, luz="#f2a65a"):
    """Taxi negro con techo amarillo, vista lateral."""
    s = esc
    tr = f' transform="translate({x},{y}) scale({-s if flip else s},{s})"'
    o = [f'<g{tr}>']
    o.append('<ellipse cx="0" cy="62" rx="250" ry="14" fill="#000" opacity="0.6"/>')
    o.append('<path d="M-230,40 L-235,0 Q-230,-20 -200,-26 L-130,-34 L-80,-86 Q-70,-96 -50,-96 L80,-96 Q100,-96 115,-80 L160,-34 L215,-26 Q240,-20 240,0 L238,40 Z" fill="#0c0d10"/>')
    # techo amarillo
    o.append('<path d="M-78,-86 Q-70,-96 -50,-96 L80,-96 Q100,-96 112,-84 L108,-80 L-74,-80 Z" fill="#e8b923"/>')
    # letrero TAXI
    o.append('<rect x="-30" y="-118" width="66" height="22" rx="4" fill="#f4d35e"/>')
    o.append('<text x="3" y="-101" font-family="DejaVu Sans" font-weight="bold" font-size="16" text-anchor="middle" fill="#1a1405">TAXI</text>')
    # ventanas
    o.append('<path d="M-70,-76 L-30,-76 L-30,-36 L-112,-36 Z" fill="#1d2735"/>')
    o.append('<path d="M-20,-76 L70,-76 L70,-36 L-20,-36 Z" fill="#1d2735"/>')
    o.append('<path d="M80,-76 L100,-76 L140,-36 L80,-36 Z" fill="#1d2735"/>')
    o.append('<path d="M-70,-76 L-50,-76 L-90,-36 L-112,-36 Z" fill="#4a5f7a" opacity="0.5"/>')
    # brillo de carrocería
    o.append(f'<path d="M-225,-8 L230,-8" stroke="{luz}" stroke-width="3" opacity="0.55"/>')
    o.append('<path d="M-130,-30 L160,-30" stroke="#59677a" stroke-width="2" opacity="0.6"/>')
    # ruedas
    for wx in (-150, 150):
        o.append(f'<circle cx="{wx}" cy="40" r="38" fill="#050506"/><circle cx="{wx}" cy="40" r="18" fill="#2a2d33"/><circle cx="{wx}" cy="40" r="6" fill="#55595f"/>')
    # luces
    o.append('<rect x="225" y="-14" width="14" height="12" fill="#fff2c8"/>')
    o.append('<rect x="-236" y="-14" width="10" height="12" fill="#b3122e"/>')
    o.append('</g>')
    return "".join(o)


# ---------------------------------------------------------------------------

def plaza_noche(path=None, sin_post=False):
    d1, sky = cielo(y_bot=720)
    body = [sky,
            via_lactea(1150, 150, 760, 150, -14, 5),
            estrellas(650, 11, y_max=620),
            cerro(630, 250, 21, "#0c1320", rim="#3a5170", rough=1.2),
            cerro(690, 150, 22, "#080c13", rough=1.0),
            edificios(705, 4, hmin=50, hmax=120),
            catedral(380, 705, esc=1.0),
            ]
    # suelo de la plaza (baldosas en perspectiva)
    body.append(f'<rect y="700" width="{W}" height="{H-700}" fill="#0d1016"/>')
    vx, vy = 900, 650
    for k in range(-26, 27):
        x2 = vx + k * 130
        body.append(f'<line x1="{vx}" y1="{vy}" x2="{x2}" y2="{H}" stroke="#171c25" stroke-width="2" opacity="0.8"/>')
    yy, step = 712, 8
    while yy < H:
        body.append(f'<line x1="0" y1="{yy:.0f}" x2="{W}" y2="{yy:.0f}" stroke="#171c25" stroke-width="2" opacity="0.7"/>')
        step *= 1.32
        yy += step
    # pimientos de fondo
    body.append(pimiento(1000, 470, 380, 260, 31, base="#0a110d", hoja="#111c15", tronco_y=715, densidad=0.45))
    body.append(pimiento(130, 480, 420, 260, 33, base="#0a110d", hoja="#111c15", tronco_y=718, densidad=0.45))
    # fuente con estatua
    body.append(estatua_mineria(640, 790, esc=0.62))
    # faroles
    body.append(farol(1080, 745, 200, escala=0.55))
    body.append(farol(250, 880, 380, escala=1.05))
    body.append(farol(1840, 870, 360, escala=1.0))
    # bancas
    body.append(banca(430, 880, 0.9, luz="#f2a65a"))
    body.append(banca(1580, 935, 0.9, luz="#f2a65a"))
    # gran pimiento (donde espera ella)
    body.append('<ellipse cx="1300" cy="860" rx="420" ry="180" fill="#000" opacity="0.6" filter="url(#b60)"/>')
    body.append(pimiento(1340, -110, 880, 940, 7, base="#0a120f", hoja="#14211a", luz="#2e2b19", tronco_y=935,
                         densidad=1.2, luz_x=1840))
    # pimiento de primer plano (esquina superior izquierda)
    body.append(pimiento(-120, -330, 900, 820, 9, base="#050907", hoja="#0b140e", luz="#2c2816", tronco_y=-200,
                         densidad=0.9, luz_x=250))
    # bruma cálida a la altura de los faroles
    body.append('<rect y="640" width="1920" height="140" fill="#f2a65a" opacity="0.05" filter="url(#b30)"/>')
    svg = doc("".join(body), d1)
    p = path or f"{BG}/plaza_noche.png"
    render(svg, p)
    if not sin_post:
        post(p, grain=7, vignette=0.6, tint=((6, 12, 28), (255, 190, 120)), seed=10)


def muro_cementerio():
    d1, sky = cielo(y_bot=760, top="#020309", mid="#081120", bot="#132136")
    body = [sky, via_lactea(500, 130, 800, 150, 12, 15), estrellas(700, 12, y_max=620),
            cerro(660, 260, 41, "#0a1019", rim="#2c3f57", rough=1.3),
            cerro(700, 140, 42, "#070b11")]
    # cosas tras el muro: cipreses, cruces y mausoleos
    tras = []
    rnd = random.Random(44)
    for i in range(16):
        x = 200 + i * 95 + rnd.uniform(-20, 20)
        t = x / 1550
        ytop = 330 + (610 - 330) * t
        alto = rnd.uniform(160, 300) * (1 - t * 0.55)
        tras.append(ciprés(x, ytop + 30, alto, alto * 0.22, "#05080a", seed=i))
    for i in range(10):
        x = 120 + i * 140 + rnd.uniform(-30, 30)
        t = x / 1550
        ytop = 330 + (610 - 330) * t
        sc = 1 - t * 0.6
        if rnd.random() < 0.5:
            tras.append(f'<rect x="{x-3*sc:.0f}" y="{ytop-70*sc:.0f}" width="{6*sc:.0f}" height="{80*sc:.0f}" fill="#06090c"/>'
                        f'<rect x="{x-20*sc:.0f}" y="{ytop-52*sc:.0f}" width="{40*sc:.0f}" height="{6*sc:.0f}" fill="#06090c"/>')
        else:
            tras.append(f'<path d="M{x-40*sc:.0f},{ytop+5:.0f} L{x-40*sc:.0f},{ytop-40*sc:.0f} A{40*sc:.0f},{40*sc:.0f} 0 0 1 {x+40*sc:.0f},{ytop-40*sc:.0f} L{x+40*sc:.0f},{ytop+5:.0f} Z" fill="#06090c"/>')
    body += tras
    # muro
    body.append('<path d="M0,330 L1550,610 L1550,700 L0,960 Z" fill="#b9b4a8"/>')
    defs = d1 + ('<linearGradient id="muroLuz" x1="0" y1="0" x2="1" y2="0">'
                 '<stop offset="0" stop-color="#000" stop-opacity="0.75"/><stop offset="0.22" stop-color="#000" stop-opacity="0.05"/>'
                 '<stop offset="0.42" stop-color="#000" stop-opacity="0.2"/><stop offset="0.75" stop-color="#000" stop-opacity="0.85"/>'
                 '<stop offset="1" stop-color="#000" stop-opacity="0.95"/></linearGradient>'
                 '<clipPath id="clipMuro"><path d="M0,330 L1550,610 L1550,700 L0,960 Z"/></clipPath>')
    # manchas de cal
    manchas = []
    for i in range(70):
        x = rnd.uniform(0, 1550)
        t = x / 1550
        ytop = 330 + 280 * t
        ybot = 960 - 260 * t
        y = rnd.uniform(ytop, ybot)
        manchas.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(20,90)*(1-t*0.6):.0f}" ry="{rnd.uniform(10,50)*(1-t*0.6):.0f}" fill="{rnd.choice(["#7d786d","#9a9486","#cfcabd","#6b675e"])}" opacity="{rnd.uniform(0.15,0.4):.2f}" filter="url(#b8)"/>')
    # chorreado bajo la cornisa
    for i in range(40):
        x = rnd.uniform(0, 1500)
        t = x / 1550
        ytop = 330 + 280 * t + 22 * (1 - t)
        manchas.append(f'<rect x="{x:.0f}" y="{ytop:.0f}" width="{rnd.uniform(3,9)*(1-t*0.6):.0f}" height="{rnd.uniform(30,140)*(1-t*0.6):.0f}" fill="#5f5a50" opacity="{rnd.uniform(0.15,0.35):.2f}" filter="url(#b2)"/>')
    body.append('<g clip-path="url(#clipMuro)">' + "".join(manchas) +
                '<rect width="1920" height="1080" fill="url(#muroLuz)"/>'
                '<ellipse cx="640" cy="610" rx="520" ry="330" fill="#f3a35a" opacity="0.38" filter="url(#b60)"/></g>')
    # cornisa
    body.append('<path d="M0,318 L1550,604 L1550,614 L0,342 Z" fill="#6f6a60"/>')
    body.append('<path d="M0,342 L1550,614 L1550,618 L0,352 Z" fill="#2a2823" opacity="0.8"/>')
    # vereda de tierra
    body.append('<path d="M0,960 L1550,700 L1920,700 L1920,722 L0,1080 Z" fill="#2b2620"/>')
    body.append('<path d="M0,1080 L1920,722 L1920,1080 Z" fill="#101215"/>')
    # solera
    body.append('<path d="M0,1068 L1920,716 L1920,724 L0,1080 Z" fill="#4c4a45"/>')
    # líneas de calle
    body.append('<path d="M1920,880 L1000,1080 L1110,1080 L1920,905 Z" fill="#c9c2a5" opacity="0.14"/>')
    # portón lejano del cementerio
    body.append('<path d="M1490,700 L1490,612 A26,26 0 0 1 1542,612 L1542,700 Z" fill="#030405"/>')
    body.append('<rect x="1484" y="590" width="64" height="8" fill="#8d887d"/>')
    # sombra del poste sobre el muro
    body.append('<path d="M650,995 L700,560 L712,560 L664,995 Z" fill="#000" opacity="0.25" filter="url(#b4)"/>')
    # faroles
    body.append(farol(640, 1000, 520, escala=1.15))
    body.append(farol(1300, 712, 160, escala=0.38, glow=False))
    body.append('<circle cx="1300" cy="560" r="5" fill="#5d4a32"/>')
    # polvo / viento
    for i in range(60):
        x = rnd.uniform(200, 1100)
        y = rnd.uniform(700, 1050)
        body.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(30,120):.0f}" ry="{rnd.uniform(3,8):.0f}" fill="#d9b88a" opacity="{rnd.uniform(0.03,0.09):.2f}" filter="url(#b8)"/>')
    # oscuridad final al fondo
    body.append('<rect x="1450" y="500" width="470" height="300" fill="#000" opacity="0.35" filter="url(#b60)"/>')
    svg = doc("".join(body), defs)
    p = f"{BG}/muro_cementerio.png"
    render(svg, p)
    post(p, grain=8, vignette=0.65, tint=((5, 10, 24), (255, 180, 110)), seed=11)


def fachada(side, vx, vy, seed, x_near_top=250, x_near_bot=880, largo=0.93):
    """Banda de edificios a un lado de la avenida, en perspectiva."""
    rnd = random.Random(seed)
    o = []
    xn = 0 if side < 0 else W
    n = 10
    for k in range(n):
        t1 = (k / n) ** 0.55 * largo
        t2 = ((k + 1) / n) ** 0.55 * largo
        xa = xn + (vx - xn) * t1
        xb = xn + (vx - xn) * t2
        yb_a = x_near_bot + (vy + 6 - x_near_bot) * t1
        yb_b = x_near_bot + (vy + 6 - x_near_bot) * t2
        hfac = rnd.uniform(0.55, 1.15)
        yt_a = yb_a - (x_near_bot - x_near_top) * (1 - t1) * hfac
        yt_b = yb_b - (x_near_bot - x_near_top) * (1 - t2) * hfac
        col = rnd.choice(["#101724", "#0d1420", "#131b29"])
        o.append(f'<path d="M{xa:.0f},{yb_a:.0f} L{xa:.0f},{yt_a:.0f} L{xb:.0f},{yt_b:.0f} L{xb:.0f},{yb_b:.0f} Z" fill="{col}"/>')
        o.append(f'<path d="M{xa:.0f},{yt_a:.0f} L{xb:.0f},{yt_b:.0f}" stroke="#2b3b52" stroke-width="2" opacity="0.7"/>')
        o.append(f'<line x1="{xa:.0f}" y1="{yt_a:.0f}" x2="{xa:.0f}" y2="{yb_a:.0f}" stroke="#05070b" stroke-width="3"/>')
        # ventanas
        filas = rnd.randint(1, 3)
        for f in range(filas):
            for c in range(3):
                if rnd.random() < 0.45:
                    tt = (c + 0.5) / 3
                    wx = xa + (xb - xa) * tt
                    ybot = yb_a + (yb_b - yb_a) * tt
                    ytop = yt_a + (yt_b - yt_a) * tt
                    wy = ytop + (ybot - ytop) * (0.2 + 0.25 * f)
                    ww = abs(xb - xa) * 0.16
                    wh = (ybot - ytop) * 0.12
                    lit = rnd.random() < 0.55
                    colw = rnd.choice(["#f2b766", "#ffd89a", "#e9a24f"]) if lit else "#1e2a3a"
                    o.append(f'<rect x="{wx-ww/2:.0f}" y="{wy:.0f}" width="{ww:.0f}" height="{wh:.0f}" fill="{colw}" opacity="{0.85 if lit else 0.9}"/>')
        # cortina metálica del local
        if rnd.random() < 0.6:
            o.append(f'<path d="M{xa:.0f},{yb_a:.0f} L{xa:.0f},{yb_a-(yb_a-yt_a)*0.28:.0f} L{xb:.0f},{yb_b-(yb_b-yt_b)*0.28:.0f} L{xb:.0f},{yb_b:.0f} Z" fill="#1b222c" opacity="0.9"/>')
    return "".join(o)


def avenida_noche():
    d1, sky = cielo(y_bot=640)
    body = [sky, via_lactea(900, 120, 900, 140, -6, 25), estrellas(800, 13, y_max=560),
            cerro(560, 300, 51, "#0c1424", rim="#3a5170", rough=1.4),
            cerro(615, 170, 52, "#080d15")]
    vx, vy = 960, 610
    body.append(fachada(-1, vx, vy, 61))
    body.append(fachada(1, vx, vy, 62))
    # farmacia con cruz verde (derecha)
    body.append('<g transform="translate(1655,470)"><rect x="-16" y="-46" width="32" height="92" fill="#3df29a"/><rect x="-46" y="-16" width="92" height="32" fill="#3df29a"/></g>')
    body.append('<circle cx="1655" cy="470" r="140" fill="#3df29a" opacity="0.20" filter="url(#b30)"/>')
    body.append(texto(1655, 570, "19°", 40, fill="#ff6b4a", weight="bold"))
    body.append('<circle cx="1655" cy="560" r="50" fill="#ff6b4a" opacity="0.15" filter="url(#b16)"/>')
    # calzada
    body.append(f'<path d="M{vx-40},{vy} L{vx+40},{vy} L{W+500},{H} L{-500},{H} Z" fill="#0e1015"/>')
    # veredas
    body.append(f'<path d="M0,880 L{vx-40},{vy+6} L{vx-40},{vy} L0,860 Z" fill="#23211d"/>')
    body.append(f'<path d="M{W},880 L{vx+40},{vy+6} L{vx+40},{vy} L{W},860 Z" fill="#23211d"/>')
    body.append(f'<path d="M0,880 L{vx-40},{vy+6} L{-500},{H} Z" fill="#141519"/>')
    body.append(f'<path d="M{W},880 L{vx+40},{vy+6} L{W+500},{H} Z" fill="#141519"/>')
    # bandejón central
    body.append(f'<path d="M{vx-5},{vy} L{vx+5},{vy} L{vx+110},{H} L{vx-110},{H} Z" fill="#1c1913"/>')
    # líneas discontinuas
    for side in (-1, 1):
        for k in range(14):
            t = (k / 14) ** 1.8
            t2 = ((k + 0.45) / 14) ** 1.8
            x1 = vx + side * (22 + 560 * t)
            y1 = vy + (H - vy) * t
            x2 = vx + side * (22 + 560 * t2)
            y2 = vy + (H - vy) * t2
            body.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#c8c0a0" stroke-width="{1+8*t:.1f}" opacity="0.55"/>')
    # faroles de sodio en las veredas
    for k in range(7):
        t = (k / 7) ** 0.6 * 0.93
        for side in (-1, 1):
            xn = 120 if side < 0 else W - 120
            x = xn + (vx - xn) * t
            yg = 900 + (vy + 8 - 900) * t
            esc = (1 - t) * 1.05 + 0.04
            body.append(farol(x, yg, 470 * esc, escala=esc))
    # resplandor naranja sobre la calzada
    body.append(f'<path d="M{vx-40},{vy} L{vx+40},{vy} L{W+500},{H} L{-500},{H} Z" fill="#f2a65a" opacity="0.07"/>')
    # auto lejano (luces rojas)
    body.append('<circle cx="935" cy="660" r="4" fill="#ff3030"/><circle cx="952" cy="660" r="4" fill="#ff3030"/>')
    body.append('<ellipse cx="944" cy="660" rx="40" ry="14" fill="#ff3030" opacity="0.3" filter="url(#b8)"/>')
    svg = doc("".join(body), d1)
    p = f"{BG}/avenida_noche.png"
    render(svg, p)
    post(p, grain=7, vignette=0.6, tint=((6, 10, 26), (255, 185, 115)), seed=12)


if __name__ == "__main__":
    names = sys.argv[1:] or ["plaza_noche", "muro_cementerio", "avenida_noche"]
    for n in names:
        globals()[n]()
        print("ok", n)


# ===========================================================================
#  Interiores y cementerio
# ===========================================================================

def casa_noche():
    defs = ('<linearGradient id="pared" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a2522"/>'
            '<stop offset="0.55" stop-color="#4a3a2c"/><stop offset="1" stop-color="#231d19"/></linearGradient>'
            '<linearGradient id="cieloV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#03050b"/><stop offset="1" stop-color="#14223a"/></linearGradient>'
            '<radialGradient id="lampara" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffcf8a" stop-opacity="0.55"/><stop offset="1" stop-color="#ffcf8a" stop-opacity="0"/></radialGradient>')
    b = []
    b.append('<rect width="1920" height="1080" fill="url(#pared)"/>')
    # zócalo y piso de tablas
    b.append('<rect y="860" width="1920" height="220" fill="#1c1410"/>')
    for k in range(14):
        x = k * 150
        b.append(f'<line x1="{x}" y1="860" x2="{x-200 + k*14}" y2="1080" stroke="#0f0b08" stroke-width="3"/>')
    b.append('<rect y="840" width="1920" height="22" fill="#14100c"/>')
    # ventana
    b.append('<rect x="250" y="170" width="560" height="520" fill="#120d0a"/>')
    b.append('<rect x="275" y="195" width="510" height="470" fill="url(#cieloV)"/>')
    b.append(f'<g clip-path="url(#clipV)">{estrellas(160, 77, y_max=520, w=1920)}</g>')
    defs += '<clipPath id="clipV"><rect x="275" y="195" width="510" height="470"/></clipPath>'
    # cerros con luces de poblaciones
    rnd = random.Random(8)
    cer = '<path d="M275,560 L340,500 L420,470 L520,430 L600,455 L680,420 L785,470 L785,665 L275,665 Z" fill="#0b0f17"/>'
    luces = "".join(f'<circle cx="{rnd.uniform(285,780):.0f}" cy="{rnd.uniform(480,660):.0f}" r="{rnd.choice([1.5,2,2.5])}" fill="{rnd.choice(["#ffb35c","#ffd08a","#f29a4a"])}" opacity="{rnd.uniform(0.5,1):.2f}"/>' for _ in range(90))
    b.append(f'<g clip-path="url(#clipV)">{cer}{luces}</g>')
    b.append('<rect x="522" y="195" width="16" height="470" fill="#120d0a"/><rect x="275" y="420" width="510" height="14" fill="#120d0a"/>')
    # cortina
    b.append('<path d="M230,150 C260,300 230,500 270,720 L200,720 C180,500 210,300 190,150 Z" fill="#3b2a2a"/>')
    b.append('<path d="M830,150 C800,300 830,500 790,720 L860,720 C880,500 850,300 870,150 Z" fill="#3b2a2a"/>')
    b.append('<rect x="170" y="140" width="720" height="16" rx="6" fill="#140e0b"/>')
    # luz de luna entrando
    b.append('<path d="M275,665 L785,665 L980,1080 L120,1080 Z" fill="#9fc2e8" opacity="0.06"/>')
    # sillón junto a la ventana
    b.append('<path d="M120,900 L120,640 Q120,600 170,600 L330,600 Q380,600 380,640 L380,900 Z" fill="#2d1f1a"/>')
    b.append('<rect x="95" y="720" width="70" height="200" rx="20" fill="#24180f"/><rect x="335" y="720" width="70" height="200" rx="20" fill="#24180f"/>')
    b.append('<rect x="150" y="760" width="200" height="60" rx="10" fill="#3a2a22"/>')
    # calendario con el 8 marcado
    b.append('<rect x="980" y="230" width="170" height="220" fill="#d9d1bf"/><rect x="980" y="230" width="170" height="44" fill="#9b1f2a"/>')
    b.append(texto(1065, 262, "NOVIEMBRE", 20, fill="#f4ead6", weight="bold", spacing=1))
    for i in range(30):
        cx_ = 995 + (i % 7) * 22
        cy_ = 300 + (i // 7) * 30
        b.append(f'<rect x="{cx_}" y="{cy_}" width="12" height="10" fill="#6d6458" opacity="0.6"/>')
    b.append('<circle cx="1001" cy="335" r="13" fill="none" stroke="#b3122e" stroke-width="3"/>')
    # reloj de pared
    b.append('<circle cx="1300" cy="200" r="48" fill="#1c1612"/><circle cx="1300" cy="200" r="40" fill="#e3dccb"/>')
    b.append('<line x1="1300" y1="200" x2="1300" y2="170" stroke="#1a1a1a" stroke-width="4"/><line x1="1300" y1="200" x2="1318" y2="208" stroke="#1a1a1a" stroke-width="4"/>')
    # repisa con fotos y radio
    b.append('<rect x="1400" y="520" width="440" height="18" fill="#1a120d"/>')
    b.append('<path d="M1420,538 L1440,580 L1450,538 Z M1800,538 L1810,580 L1830,538 Z" fill="#1a120d"/>')
    b.append('<rect x="1440" y="410" width="90" height="110" fill="#3a2a1c"/><rect x="1452" y="422" width="66" height="86" fill="#8f8574"/>')
    b.append('<ellipse cx="1485" cy="452" rx="16" ry="20" fill="#5f5649"/><path d="M1462,508 Q1485,470 1508,508 Z" fill="#5f5649"/>')
    # foto boca abajo
    b.append('<rect x="1560" y="506" width="110" height="14" fill="#2a1d12"/>')
    b.append('<rect x="1570" y="498" width="90" height="10" fill="#3a2a1c"/>')
    # radio antigua
    b.append('<rect x="1700" y="430" width="130" height="90" rx="14" fill="#4a3322"/><rect x="1712" y="444" width="70" height="62" rx="6" fill="#2a1c12"/>')
    b.append('<circle cx="1805" cy="462" r="10" fill="#c9a06a"/><circle cx="1805" cy="492" r="10" fill="#c9a06a"/>')
    # mesa con lámpara
    b.append('<rect x="1180" y="720" width="380" height="20" fill="#2a1c13"/><rect x="1200" y="740" width="16" height="140" fill="#21160f"/><rect x="1524" y="740" width="16" height="140" fill="#21160f"/>')
    b.append('<rect x="1200" y="700" width="340" height="24" fill="#6f3a2e" opacity="0.8"/>')
    b.append('<path d="M1330,700 L1350,620 L1370,620 L1390,700 Z" fill="#2b1f17"/>')
    b.append('<path d="M1295,630 L1425,630 L1395,550 L1325,550 Z" fill="#e7c48c"/>')
    b.append('<circle cx="1360" cy="600" r="420" fill="url(#lampara)"/>')
    b.append('<circle cx="1360" cy="600" r="120" fill="#ffd08a" opacity="0.25" filter="url(#b30)"/>')
    # pan y pastillas
    b.append('<ellipse cx="1260" cy="700" rx="50" ry="12" fill="#c2b49a"/><ellipse cx="1250" cy="690" rx="22" ry="12" fill="#c98f4e"/><ellipse cx="1278" cy="692" rx="20" ry="11" fill="#b8783e"/>')
    b.append('<ellipse cx="1470" cy="702" rx="28" ry="8" fill="#e8e2d6"/><circle cx="1462" cy="699" r="4" fill="#f4f0ff"/><circle cx="1476" cy="700" r="4" fill="#ffd9d9"/>')
    # puerta a la derecha
    b.append('<rect x="1880" y="200" width="60" height="660" fill="#1a120c"/>')
    # sombra general en bordes
    b.append('<rect width="1920" height="1080" fill="#000" opacity="0.18"/>')
    svg = doc("".join(b), defs)
    p = f"{BG}/casa_noche.png"
    render(svg, p)
    post(p, grain=7, vignette=0.65, tint=((12, 10, 24), (255, 200, 140)), seed=14)


def _calle_por_parabrisas():
    """Vista nocturna hacia adelante (se recorta con el parabrisas)."""
    b = []
    b.append('<rect width="1920" height="620" fill="url(#cieloT)"/>')
    b.append(estrellas(300, 91, y_max=330))
    b.append(cerro(400, 150, 92, "#0c1424", rim="#33465f"))
    vx, vy = 960, 450
    b.append(fachada(-1, vx, vy, 93, x_near_top=40, x_near_bot=640, largo=0.9))
    b.append(fachada(1, vx, vy, 94, x_near_top=40, x_near_bot=640, largo=0.9))
    b.append(f'<path d="M{vx-30},{vy} L{vx+30},{vy} L1700,620 L220,620 Z" fill="#0f1116"/>')
    for k in range(6):
        t = (k / 6) ** 0.6 * 0.9
        for side in (-1, 1):
            xn = 60 if side < 0 else 1860
            x = xn + (vx - xn) * t
            yg = 640 + (vy + 6 - 640) * t
            esc = (1 - t) * 0.8 + 0.05
            b.append(farol(x, yg, 420 * esc, escala=esc))
    for k in range(6):
        t = (k / 6) ** 1.7
        y1 = vy + (620 - vy) * t
        b.append(f'<line x1="{vx}" y1="{y1:.0f}" x2="{vx}" y2="{y1 + 4 + 30*t:.0f}" stroke="#c8c0a0" stroke-width="{1+6*t:.1f}" opacity="0.6"/>')
    return "".join(b)


def taxi_frente(detenido=False):
    defs = ('<linearGradient id="cieloT" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02040a"/><stop offset="1" stop-color="#14223a"/></linearGradient>'
            '<clipPath id="parabrisas"><path d="M180,40 L1740,40 L1900,600 L20,600 Z"/></clipPath>'
            '<clipPath id="espejoC"><rect x="790" y="62" width="340" height="104" rx="22"/></clipPath>'
            '<linearGradient id="tablero" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16171b"/><stop offset="1" stop-color="#050506"/></linearGradient>')
    b = []
    b.append('<rect width="1920" height="1080" fill="#050507"/>')
    b.append(f'<g clip-path="url(#parabrisas)">{_calle_por_parabrisas()}'
             '<rect width="1920" height="620" fill="#7fa6d6" opacity="0.04"/>'
             '<path d="M300,40 L700,40 L380,600 L120,600 Z" fill="#ffffff" opacity="0.03"/></g>')
    # pilares y techo
    b.append('<path d="M0,0 L1920,0 L1920,40 L0,40 Z" fill="#0b0b0e"/>')
    b.append('<path d="M0,0 L190,40 L30,600 L0,620 Z" fill="#0a0a0d"/>')
    b.append('<path d="M1920,0 L1730,40 L1890,600 L1920,620 Z" fill="#0a0a0d"/>')
    # espejo retrovisor
    b.append('<rect x="950" y="30" width="20" height="40" fill="#111"/>')
    b.append('<rect x="780" y="54" width="360" height="120" rx="28" fill="#0d0d10"/>')
    reflejo = ('<rect x="790" y="62" width="340" height="104" fill="#121722"/>'
               '<path d="M790,140 L1130,140 L1130,166 L790,166 Z" fill="#2a1418"/>'
               '<rect x="860" y="72" width="200" height="50" rx="14" fill="#1e2b3e"/>'
               '<circle cx="900" cy="96" r="7" fill="#f2a65a" opacity="0.8"/><circle cx="1010" cy="92" r="5" fill="#f2a65a" opacity="0.6"/>')
    b.append(f'<g clip-path="url(#espejoC)">{reflejo}</g>')
    b.append('<rect x="790" y="62" width="340" height="104" rx="22" fill="none" stroke="#2a2d33" stroke-width="3"/>')
    # rosario colgando
    cuentas = []
    for i in range(22):
        t = i / 21
        ang = math.pi * t
        x = 930 + 40 * math.cos(ang) * 0.9
        y = 176 + 120 * math.sin(ang) * 0.95
        cuentas.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="#6b4b8a"/>')
    b.append("".join(cuentas))
    b.append('<line x1="930" y1="296" x2="930" y2="330" stroke="#6b4b8a" stroke-width="3"/>')
    b.append('<rect x="926" y="330" width="8" height="34" fill="#c9b27a"/><rect x="917" y="340" width="26" height="7" fill="#c9b27a"/>')
    # tablero
    b.append('<path d="M0,620 Q960,520 1920,620 L1920,1080 L0,1080 Z" fill="url(#tablero)"/>')
    b.append('<path d="M0,620 Q960,520 1920,620" stroke="#2c2f36" stroke-width="3" fill="none"/>')
    # instrumentos tras el volante
    b.append('<ellipse cx="520" cy="760" rx="230" ry="90" fill="#08090b"/>')
    b.append('<circle cx="450" cy="760" r="60" fill="#0d0f13" stroke="#2a2e36" stroke-width="3"/><circle cx="600" cy="760" r="60" fill="#0d0f13" stroke="#2a2e36" stroke-width="3"/>')
    b.append('<line x1="450" y1="760" x2="415" y2="790" stroke="#ff7a2a" stroke-width="3"/><line x1="600" y1="760" x2="570" y2="735" stroke="#ff7a2a" stroke-width="3"/>')
    b.append('<circle cx="450" cy="760" r="60" fill="#ff7a2a" opacity="0.05"/>')
    # volante
    b.append('<path d="M140,1080 A390,390 0 0 1 900,1080" stroke="#0c0c0f" stroke-width="58" fill="none"/>')
    b.append('<path d="M150,1060 A380,380 0 0 1 400,740" stroke="#2c2e34" stroke-width="5" fill="none" opacity="0.7"/>')
    b.append('<path d="M520,1080 L520,960 Q520,920 560,910 L760,880" stroke="#0c0c0f" stroke-width="44" fill="none"/>')
    # radio
    b.append('<rect x="860" y="690" width="260" height="90" rx="8" fill="#0b0c0f" stroke="#2a2d33" stroke-width="2"/>')
    b.append('<rect x="880" y="705" width="160" height="40" rx="4" fill="#0e2a1c"/>')
    b.append(texto(960, 736, "88.5 FM" if not detenido else "- - - -", 26, fill="#5cf2a0", font="DejaVu Sans Mono", weight="bold"))
    b.append('<rect x="880" y="705" width="160" height="40" fill="#5cf2a0" opacity="0.12" filter="url(#b8)"/>')
    b.append('<circle cx="1080" cy="725" r="18" fill="#1a1c21"/><circle cx="1080" cy="725" r="6" fill="#3a3d44"/>')
    # reloj del tablero
    hora = "23:47" if detenido else "23:41"
    b.append('<rect x="905" y="610" width="110" height="48" rx="6" fill="#0a0506"/>')
    b.append(texto(960, 646, hora, 32, fill="#ff3b30", font="DejaVu Sans Mono", weight="bold"))
    b.append('<rect x="905" y="610" width="110" height="48" fill="#ff3b30" opacity="0.18" filter="url(#b8)"/>')
    # taxímetro
    b.append('<rect x="1300" y="560" width="300" height="110" rx="10" fill="#0b0b0d" stroke="#2c2f36" stroke-width="3"/>')
    b.append('<rect x="1320" y="580" width="260" height="60" rx="4" fill="#160404"/>')
    tarifa = "E° 0,00" if detenido else "$ 450"
    b.append(texto(1450, 624, tarifa, 40, fill="#ff3b30", font="DejaVu Sans Mono", weight="bold"))
    b.append('<rect x="1320" y="580" width="260" height="60" fill="#ff3b30" opacity="0.18" filter="url(#b8)"/>')
    b.append(texto(1450, 662, "TARIFA", 14, fill="#6f737c", font="DejaVu Sans", spacing=4))
    # reflejos de luz de calle sobre el tablero
    b.append('<path d="M0,640 Q960,560 1920,640 L1920,660 Q960,580 0,660 Z" fill="#f2a65a" opacity="0.10"/>')
    b.append('<rect width="1920" height="1080" fill="#000" opacity="0.08"/>')
    svg = doc("".join(b), defs)
    p = f"{BG}/taxi_frente{'_detenido' if detenido else ''}.png"
    render(svg, p)
    post(p, grain=7, vignette=0.55, tint=((6, 8, 20), (255, 180, 110)), seed=15)


def taxi_atras():
    defs = ('<clipPath id="lunetaC"><path d="M420,110 L1500,110 Q1560,110 1580,170 L1640,430 L280,430 L340,170 Q360,110 420,110 Z"/></clipPath>'
            '<linearGradient id="asientoG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#241619"/><stop offset="1" stop-color="#0a0607"/></linearGradient>')
    rnd = random.Random(101)
    b = ['<rect width="1920" height="1080" fill="#060607"/>']
    luneta = ['<rect width="1920" height="450" fill="#0a1222"/>', estrellas(120, 102, y_max=250)]
    for i in range(26):
        x = rnd.uniform(300, 1620)
        y = rnd.uniform(280, 420)
        r = rnd.uniform(14, 46)
        col = rnd.choice(["#f2a65a", "#ffcf8a", "#ff6a3a", "#9fd0ff"])
        luneta.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{col}" opacity="{rnd.uniform(0.15,0.45):.2f}" filter="url(#b4)"/>')
    luneta.append('<rect y="380" width="1920" height="60" fill="#111" />')
    b.append(f'<g clip-path="url(#lunetaC)">{"".join(luneta)}</g>')
    b.append('<path d="M420,110 L1500,110 Q1560,110 1580,170 L1640,430 L280,430 L340,170 Q360,110 420,110 Z" fill="none" stroke="#141418" stroke-width="10"/>')
    # pilares laterales y ventanas de puertas
    b.append('<path d="M0,0 L380,0 L260,470 L0,560 Z" fill="#0b0b0e"/>')
    b.append('<path d="M1920,0 L1540,0 L1660,470 L1920,560 Z" fill="#0b0b0e"/>')
    b.append('<path d="M40,160 L220,120 L170,420 L40,470 Z" fill="#101a2a"/>')
    b.append('<path d="M1880,160 L1700,120 L1750,420 L1880,470 Z" fill="#101a2a"/>')
    b.append('<circle cx="120" cy="300" r="40" fill="#f2a65a" opacity="0.35" filter="url(#b16)"/>')
    # bandeja trasera
    b.append('<path d="M260,430 L1660,430 L1720,520 L200,520 Z" fill="#0d0d10"/>')
    # respaldo del asiento
    b.append('<path d="M150,520 L1770,520 Q1800,520 1800,560 L1820,880 L100,880 L120,560 Q120,520 150,520 Z" fill="url(#asientoG)"/>')
    for x in (700, 1220):
        b.append(f'<path d="M{x},525 L{x+10},880" stroke="#050304" stroke-width="5"/>')
    for k in range(5):
        y = 580 + k * 60
        b.append(f'<path d="M140,{y} Q960,{y-12} 1780,{y}" stroke="#2e1b20" stroke-width="2" fill="none" opacity="0.7"/>')
    # cojín
    b.append('<path d="M60,860 L1860,860 Q1900,870 1900,920 L1920,1080 L0,1080 L20,920 Q20,870 60,860 Z" fill="#1a0f12"/>')
    b.append('<path d="M60,860 L1860,860" stroke="#3a242a" stroke-width="4"/>')
    # banda de luz de farol cruzando
    b.append('<path d="M0,600 L1920,420 L1920,520 L0,720 Z" fill="#f2a65a" opacity="0.10" filter="url(#b16)"/>')
    # cinturones colgando
    b.append('<path d="M240,470 L260,900" stroke="#101012" stroke-width="18"/><path d="M1680,470 L1660,900" stroke="#101012" stroke-width="18"/>')
    b.append('<rect width="1920" height="1080" fill="#000" opacity="0.12"/>')
    svg = doc("".join(b), defs)
    p = f"{BG}/taxi_atras.png"
    render(svg, p)
    post(p, grain=7, vignette=0.7, tint=((8, 6, 18), (255, 170, 120)), seed=16)


def paradero_noche():
    d1, sky = cielo(y_bot=700)
    b = [sky, estrellas(500, 121, y_max=420), cerro(520, 200, 122, "#0b111b", rim="#33465f"),
         cerro(560, 110, 123, "#080c13")]
    # edificio del terminal
    b.append('<rect x="600" y="420" width="1320" height="300" fill="#121822"/>')
    b.append('<rect x="600" y="410" width="1320" height="16" fill="#1d2633"/>')
    for i in range(10):
        x = 640 + i * 125
        lit = i in (2, 3, 6, 7, 8)
        b.append(f'<rect x="{x}" y="520" width="90" height="150" fill="{"#d6e6f2" if lit else "#1b2533"}" opacity="{0.55 if lit else 1}"/>')
    b.append('<rect x="900" y="440" width="720" height="58" fill="#0c1018"/>')
    b.append(texto(1260, 484, "TERMINAL DE BUSES", 40, fill="#bfe3ff", font="DejaVu Sans", weight="bold", spacing=6))
    b.append('<rect x="900" y="440" width="720" height="58" fill="#7cc7ff" opacity="0.15" filter="url(#b16)"/>')
    # calle y vereda
    b.append('<rect y="700" width="1920" height="380" fill="#0e1015"/>')
    b.append('<rect y="700" width="1920" height="60" fill="#1d1b18"/>')
    b.append('<rect y="756" width="1920" height="8" fill="#3b3935"/>')
    # taxis estacionados
    b.append(taxi_chileno(1430, 820, esc=1.0, luz="#cfe6ff"))
    b.append(taxi_chileno(1830, 830, esc=1.05, luz="#cfe6ff"))
    # toldo del paradero
    b.append('<rect x="120" y="360" width="760" height="26" fill="#1c232c"/>')
    b.append('<path d="M100,340 L900,340 L880,362 L120,362 Z" fill="#2a3340"/>')
    b.append('<rect x="150" y="386" width="14" height="400" fill="#141a22"/><rect x="836" y="386" width="14" height="400" fill="#141a22"/>')
    # tubo fluorescente
    b.append('<rect x="300" y="388" width="420" height="10" rx="5" fill="#effff6"/>')
    b.append('<ellipse cx="510" cy="400" rx="300" ry="60" fill="#c8ffe6" opacity="0.35" filter="url(#b16)"/>')
    b.append('<path d="M300,398 L720,398 L900,900 L120,900 Z" fill="#cdfff0" opacity="0.07"/>')
    b.append('<ellipse cx="510" cy="790" rx="420" ry="70" fill="url(#pozoFrio)"/>')
    # banca y termo
    b.append(banca(340, 700, 1.3, color="#11161d", luz="#bfffe8"))
    b.append('<rect x="560" y="640" width="34" height="62" rx="8" fill="#7a1f24"/><rect x="560" y="632" width="34" height="14" rx="4" fill="#c7c9cc"/>')
    # letrero
    b.append('<rect x="60" y="470" width="10" height="320" fill="#141a22"/>')
    b.append('<rect x="20" y="440" width="150" height="70" rx="6" fill="#1d4e8f"/>')
    b.append(texto(95, 486, "TAXIS", 30, fill="#ffffff", font="DejaVu Sans", weight="bold", spacing=3))
    # hervidor y vasos
    b.append('<rect x="760" y="672" width="40" height="30" rx="6" fill="#d6d9dd"/>')
    # farol cálido lejano
    b.append(farol(1700, 720, 300, escala=0.7))
    b.append('<rect width="1920" height="1080" fill="#000" opacity="0.1"/>')
    svg = doc("".join(b), d1)
    p = f"{BG}/paradero_noche.png"
    render(svg, p)
    post(p, grain=7, vignette=0.6, tint=((6, 12, 22), (200, 255, 230)), seed=17)


def cementerio_reja():
    d1, sky = cielo(y_bot=760, top="#020309", mid="#081120", bot="#132136")
    rnd = random.Random(131)
    b = [sky, via_lactea(960, 120, 900, 150, 4, 132), estrellas(700, 133, y_max=600),
         cerro(640, 260, 134, "#0a1019", rim="#2c3f57", rough=1.3), cerro(690, 140, 135, "#070b11")]
    # interior: cipreses, mausoleos, cruces
    for i in range(14):
        x = 120 + i * 130 + rnd.uniform(-30, 30)
        b.append(ciprés(x, 700, rnd.uniform(220, 380), rnd.uniform(50, 80), "#05080a", seed=i + 140))
    for i in range(8):
        x = 200 + i * 220 + rnd.uniform(-40, 40)
        sc = rnd.uniform(0.7, 1.1)
        b.append(f'<path d="M{x-60*sc},{720} L{x-60*sc},{640-40*sc} L{x},{600-60*sc} L{x+60*sc},{640-40*sc} L{x+60*sc},{720} Z" fill="#090d12"/>')
        b.append(f'<rect x="{x-3}" y="{560-60*sc}" width="6" height="50" fill="#090d12"/><rect x="{x-16}" y="{575-60*sc}" width="32" height="6" fill="#090d12"/>')
    # muro a ambos lados
    b.append('<rect x="0" y="560" width="620" height="260" fill="#a9a497"/><rect x="1300" y="560" width="620" height="260" fill="#a9a497"/>')
    b.append('<rect x="0" y="548" width="620" height="16" fill="#6f6a60"/><rect x="1300" y="548" width="620" height="16" fill="#6f6a60"/>')
    b.append('<rect x="0" y="560" width="620" height="260" fill="#000" opacity="0.45"/><rect x="1300" y="560" width="620" height="260" fill="#000" opacity="0.65"/>')
    # pórtico
    defs_extra = '<clipPath id="arcoC"><path d="M710,820 L710,560 A250,130 0 0 1 1210,560 L1210,820 Z"/></clipPath>'
    b.append('<path d="M620,820 L620,250 L1300,250 L1300,820 L1210,820 L1210,560 A250,130 0 0 0 710,560 L710,820 Z" fill="#c4bfb2"/>')
    b.append('<rect x="600" y="230" width="720" height="34" fill="#8f8a7f"/>')
    b.append('<path d="M640,232 L960,150 L1280,232 Z" fill="#b5b0a3"/>')
    b.append('<rect x="954" y="90" width="12" height="72" fill="#8f8a7f"/><rect x="935" y="108" width="50" height="10" fill="#8f8a7f"/>')
    b.append('<rect x="680" y="300" width="560" height="84" fill="#b0ab9e"/>')
    b.append(texto(960, 362, "CEMENTERIO", 56, fill="#3a372f", weight="bold", spacing=10))
    b.append('<path d="M620,820 L620,250 L1300,250 L1300,820" fill="none" stroke="#5d594f" stroke-width="4"/>')
    b.append('<path d="M1210,560 A250,130 0 0 0 960,430 L960,250 L1300,250 L1300,820 L1210,820 Z" fill="#000" opacity="0.30"/>')
    # interior oscuro bajo el arco
    b.append('<path d="M710,820 L710,560 A250,130 0 0 1 1210,560 L1210,820 Z" fill="#0c1118" opacity="0.55"/>')
    # caseta con ampolleta al fondo (a través de la reja)
    b.append('<rect x="1060" y="620" width="120" height="110" fill="#1a1d22"/><rect x="1090" y="645" width="50" height="40" fill="#ffd27a"/>')
    b.append('<circle cx="1115" cy="665" r="90" fill="#ffd27a" opacity="0.25" filter="url(#b30)"/>')
    # reja de fierro (recortada al arco)
    rej = []
    for i in range(24):
        x = 716 + i * 21
        rej.append(f'<rect x="{x}" y="420" width="6" height="400" fill="#0a0b0d"/>')
        rej.append(f'<path d="M{x-5},{470} L{x+3},{448} L{x+11},{470} Z" fill="#0a0b0d"/>')
    rej.append('<rect x="710" y="600" width="500" height="10" fill="#0a0b0d"/><rect x="710" y="750" width="500" height="10" fill="#0a0b0d"/>')
    b.append('<g clip-path="url(#arcoC)">' + "".join(rej) + '</g>')
    b.append('<path d="M710,560 A250,130 0 0 1 1210,560" stroke="#0a0b0d" stroke-width="10" fill="none"/>')
    # cadena y candado
    b.append('<path d="M944,640 Q960,628 976,640 Q960,652 944,640 Z M944,670 Q960,658 976,670 Q960,682 944,670 Z" stroke="#5a5a5a" stroke-width="5" fill="none"/>')
    b.append('<rect x="944" y="684" width="34" height="28" rx="4" fill="#3a3a3a"/>')
    # vereda y calle
    b.append('<rect y="820" width="1920" height="260" fill="#1e1b17"/><rect y="900" width="1920" height="180" fill="#0f1115"/>')
    b.append('<rect y="896" width="1920" height="8" fill="#3b3935"/>')
    # farol izquierdo
    b.append(farol(380, 900, 460, escala=1.0))
    b.append('<ellipse cx="700" cy="560" rx="420" ry="320" fill="#f3a35a" opacity="0.18" filter="url(#b60)"/>')
    b.append('<rect width="1920" height="1080" fill="#000" opacity="0.1"/>')
    svg = doc("".join(b), d1 + defs_extra)
    p = f"{BG}/cementerio_reja.png"
    render(svg, p)
    post(p, grain=8, vignette=0.65, tint=((5, 10, 24), (255, 180, 110)), seed=18)


def cementerio_pasaje(alba=False):
    VP = (960, 540)
    if alba:
        defs = ('<linearGradient id="cieloP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b4f78"/>'
                '<stop offset="0.55" stop-color="#d98c86"/><stop offset="1" stop-color="#f7c58f"/></linearGradient>')
        muroI, muroD, placa, piso = "#b8a79b", "#7d6f6a", "#e6ddd2", "#6b5a4c"
    else:
        defs = ('<linearGradient id="cieloP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#02040a"/>'
                '<stop offset="1" stop-color="#152238"/></linearGradient>')
        muroI, muroD, placa, piso = "#3c4352", "#262c38", "#7f8796", "#15161a"
    b = [f'<rect width="1920" height="1080" fill="url(#cieloP)"/>']
    if not alba:
        b.append(estrellas(200, 151, y_max=500))
    else:
        b.append('<circle cx="960" cy="560" r="300" fill="#ffd9a0" opacity="0.5" filter="url(#b60)"/>')
    # al fondo: cerros y el tocón del pimiento
    b.append(cerro(600, 120, 152, "#2a2433" if alba else "#0a1019"))
    b.append(f'<path d="M930,640 L935,600 L955,610 L975,596 L990,640 Z" fill="{"#3b2c26" if alba else "#08090b"}"/>')

    def P(side, t, hf):
        # t: 0 cerca .. 1 lejos ; hf: 0 piso .. 1 tope
        xn = -60 if side < 0 else 1980
        x = xn + (VP[0] - xn) * t
        ytop = -140 + (VP[1] + 0 - (-140)) * t
        ybot = 1220 + (VP[1] - 1220) * t
        return x, ybot + (ytop - ybot) * hf

    tmax = 0.80
    for side, col in ((-1, muroI), (1, muroD)):
        a = P(side, 0, 0); bq = P(side, 0, 1); c = P(side, tmax, 1); d = P(side, tmax, 0)
        b.append(f'<path d="M{a[0]:.0f},{a[1]:.0f} L{bq[0]:.0f},{bq[1]:.0f} L{c[0]:.0f},{c[1]:.0f} L{d[0]:.0f},{d[1]:.0f} Z" fill="{col}"/>')
    # piso
    a = P(-1, 0, 0); d = P(-1, tmax, 0); e = P(1, tmax, 0); f = P(1, 0, 0)
    b.append(f'<path d="M{a[0]:.0f},{a[1]:.0f} L{d[0]:.0f},{d[1]:.0f} L{e[0]:.0f},{e[1]:.0f} L{f[0]:.0f},{f[1]:.0f} Z" fill="{piso}"/>')
    # cuadrícula de nichos
    rnd = random.Random(160 + (1 if alba else 0))
    rnd_fijo = random.Random(160)
    cols = [0.0]
    step = 0.17
    while cols[-1] < tmax - 0.02:
        cols.append(min(tmax, cols[-1] + step))
        step *= 0.82
    filas = [0.04, 0.22, 0.40, 0.58, 0.76, 0.94]
    velas = []
    for side in (-1, 1):
        for ci in range(len(cols) - 1):
            for fi in range(len(filas) - 1):
                t1, t2 = cols[ci], cols[ci + 1]
                h1, h2 = filas[fi], filas[fi + 1]
                ins_t = (t2 - t1) * 0.08
                ins_h = (h2 - h1) * 0.10
                q = [P(side, t1 + ins_t, h1 + ins_h), P(side, t1 + ins_t, h2 - ins_h), P(side, t2 - ins_t, h2 - ins_h), P(side, t2 - ins_t, h1 + ins_h)]
                ocupado = rnd_fijo.random() < 0.85
                fill = placa if ocupado else ("#3a3030" if alba else "#0c0e12")
                shade = 1.0 if side < 0 else 0.75
                b.append(f'<path d="M{q[0][0]:.1f},{q[0][1]:.1f} L{q[1][0]:.1f},{q[1][1]:.1f} L{q[2][0]:.1f},{q[2][1]:.1f} L{q[3][0]:.1f},{q[3][1]:.1f} Z" fill="{fill}" opacity="{shade:.2f}"/>')
                if ocupado:
                    # líneas de texto
                    for k in range(2):
                        hh = h1 + ins_h + (h2 - h1 - 2 * ins_h) * (0.35 + 0.2 * k)
                        p1 = P(side, t1 + ins_t * 3, hh)
                        p2 = P(side, t2 - ins_t * 3, hh)
                        b.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#4a4744" stroke-width="{max(1, 4*(1-t1)):.1f}" opacity="0.6"/>')
                    if rnd_fijo.random() < 0.45:
                        cxp, cyp = P(side, (t1 + t2) / 2, (h1 + h2) / 2 + 0.03)
                        rr = 22 * (1 - t1) + 2
                        b.append(f'<ellipse cx="{cxp:.1f}" cy="{cyp:.1f}" rx="{rr*0.75:.1f}" ry="{rr:.1f}" fill="#d8cbb2" stroke="#8b7a55" stroke-width="{max(1,3*(1-t1)):.1f}"/>'
                                 f'<ellipse cx="{cxp:.1f}" cy="{cyp+rr*0.15:.1f}" rx="{rr*0.4:.1f}" ry="{rr*0.55:.1f}" fill="#6b5e4c" opacity="0.7"/>')
                    if rnd_fijo.random() < 0.5:
                        fx, fy = P(side, (t1 + t2) / 2, h1 + ins_h * 1.5)
                        rr = 16 * (1 - t1) + 2
                        for j in range(5):
                            b.append(f'<circle cx="{fx + rnd_fijo.uniform(-rr,rr):.1f}" cy="{fy - rnd_fijo.uniform(0,rr*1.5):.1f}" r="{rr*0.35:.1f}" fill="{rnd_fijo.choice(["#b3122e","#d86a8a","#e8c84a","#7a5ab0","#f0f0f0"])}" opacity="{0.6 if alba else 0.45}"/>')
                    if fi == 0 and rnd_fijo.random() < 0.7 or (fi == 1 and rnd_fijo.random() < 0.3):
                        vx_, vy_ = P(side, (t1 + t2) / 2 + 0.01, h1 + 0.01)
                        rr = 14 * (1 - t1) + 2
                        velas.append((vx_, vy_, rr))
    # velas en frascos
    for (x, y, rr) in velas:
        b.append(f'<rect x="{x-rr*0.6:.1f}" y="{y-rr*1.8:.1f}" width="{rr*1.2:.1f}" height="{rr*1.8:.1f}" rx="{rr*0.2:.1f}" fill="#d8e6e8" opacity="0.35"/>')
        if not alba:
            b.append(f'<ellipse cx="{x:.1f}" cy="{y-rr*2.2:.1f}" rx="{rr*0.25:.1f}" ry="{rr*0.5:.1f}" fill="#fff0c0"/>')
            b.append(f'<circle cx="{x:.1f}" cy="{y-rr*2:.1f}" r="{rr*6:.1f}" fill="url(#glowVela)" opacity="0.9"/>')
    # letrero de lata: PASAJE LOS PIMIENTOS
    sx, sy = P(-1, 0.12, 0.70)
    rot = "skewY(24)" if True else ""
    letrero_col = "#4f6f6a" if not alba else "#5f8a82"
    b.append(f'<g transform="translate({sx:.0f},{sy:.0f}) {rot}">'
             f'<rect x="-10" y="-50" width="320" height="96" rx="6" fill="{letrero_col}" stroke="#2a2420" stroke-width="5"/>'
             f'<rect x="-10" y="-50" width="320" height="96" rx="6" fill="#8a4a24" opacity="0.25"/>'
             + texto(150, -12, "PASAJE", 28, fill="#ece3cf", weight="bold", spacing=6)
             + texto(150, 28, "LOS PIMIENTOS", 30, fill="#ece3cf", weight="bold", spacing=2)
             + '</g>')
    # luz
    if alba:
        b.append('<path d="M760,420 L1160,420 L1700,1080 L220,1080 Z" fill="#ffcf9a" opacity="0.18" filter="url(#b30)"/>')
    else:
        b.append('<rect width="1920" height="1080" fill="#0a1830" opacity="0.18"/>')
        b.append('<ellipse cx="960" cy="200" rx="700" ry="200" fill="#9fc2e8" opacity="0.06" filter="url(#b60)"/>')
    svg = doc("".join(b), defs)
    p = f"{BG}/cementerio_{'alba' if alba else 'pasaje'}.png"
    render(svg, p)
    if alba:
        post(p, grain=6, vignette=0.5, tint=((40, 20, 50), (255, 210, 170)), seed=19)
    else:
        post(p, grain=8, vignette=0.65, tint=((5, 10, 24), (255, 190, 120)), seed=19)


def todo():
    plaza_noche(); muro_cementerio(); avenida_noche(); casa_noche()
    taxi_frente(False); taxi_frente(True); taxi_atras(); paradero_noche()
    cementerio_reja(); cementerio_pasaje(False); cementerio_pasaje(True)
