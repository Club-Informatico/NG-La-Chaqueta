"""Personajes de LA CHAQUETA (sprites con transparencia, 820x1080)."""
import math
import random
import sys

from lib import *

SP = OUT + "/sprites"
SW, SH = 820, 1080
LINE = "#16100f"


def sdoc(body, defs=""):
    return doc(body, defs, w=SW, h=SH)


# ---------------------------------------------------------------------------
#  Rasgos
# ---------------------------------------------------------------------------

def ojo(cx, cy, w, h, estado="neutral", lado=-1, iris="#2a1c18", blanco="#ece8ef", linea=LINE, pest=4.0,
        viejo=False, humedo=False, piel_sombra="#c9a594"):
    """Un ojo almendrado. lado=-1 (izquierda del espectador) o 1."""
    x0, x1 = cx - w / 2, cx + w / 2
    # extremo interno (hacia la nariz) un poco más bajo
    yi = cy + h * 0.10
    ye = cy - h * 0.05
    xin, xout = (x1, x0) if lado < 0 else (x0, x1)
    yin, yout = yi, ye
    up = h * (1.0 if estado == "neutral" else 0.62 if estado == "triste" else 0.75)
    lo = h * (0.45 if estado != "sonrisa" else -0.05)
    iris_dy = 0 if estado != "triste" else h * 0.18
    gid = f"eye{int(cx)}{int(cy)}{estado}"
    upper = f"M{xout:.1f},{yout:.1f} Q{cx:.1f},{cy - up*1.25:.1f} {xin:.1f},{yin:.1f}"
    lower = f"Q{cx:.1f},{cy + lo*1.3:.1f} {xout:.1f},{yout:.1f}"
    o = [f'<clipPath id="{gid}"><path d="{upper} {lower} Z"/></clipPath>']
    o.append(f'<path d="{upper} {lower} Z" fill="{blanco}"/>')
    ir = h * 0.62
    o.append(f'<g clip-path="url(#{gid})">'
             f'<circle cx="{cx + lado*0.0:.1f}" cy="{cy + iris_dy:.1f}" r="{ir:.1f}" fill="{iris}"/>'
             f'<circle cx="{cx:.1f}" cy="{cy + iris_dy:.1f}" r="{ir*0.45:.1f}" fill="#0a0606"/>'
             f'<circle cx="{cx + ir*0.35:.1f}" cy="{cy + iris_dy - ir*0.4:.1f}" r="{ir*0.26:.1f}" fill="#ffffff" opacity="0.9"/>'
             f'<path d="{upper} L{xin:.1f},{yin - h:.1f} L{xout:.1f},{yout - h:.1f} Z" fill="{piel_sombra}" opacity="0.25" transform="translate(0,{h*0.25:.1f})"/>'
             f'</g>')
    if humedo:
        o.append(f'<path d="M{cx - w*0.3:.1f},{cy + lo*0.9:.1f} Q{cx:.1f},{cy + lo*1.5:.1f} {cx + w*0.3:.1f},{cy + lo*0.9:.1f}" stroke="#ffffff" stroke-width="2" fill="none" opacity="0.8"/>')
    # línea superior (pestañas)
    o.append(f'<path d="{upper}" stroke="{linea}" stroke-width="{pest}" fill="none" stroke-linecap="round"/>')
    if pest >= 4:
        # pestañas exteriores
        o.append(f'<path d="M{xout:.1f},{yout:.1f} l{lado*-1*-7:.1f},{-5:.1f}" stroke="{linea}" stroke-width="{pest*0.7:.1f}" stroke-linecap="round"/>')
    # pliegue del párpado
    o.append(f'<path d="M{xout + (w*0.1 if lado<0 else -w*0.1):.1f},{yout - h*0.5:.1f} Q{cx:.1f},{cy - up*1.25 - h*0.55:.1f} {xin + (-w*0.15 if lado<0 else w*0.15):.1f},{yin - h*0.55:.1f}" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.45"/>')
    if estado == "sonrisa":
        o.append(f'<path d="M{xout:.1f},{yout + h*0.2:.1f} Q{cx:.1f},{cy + h*0.25:.1f} {xin:.1f},{yin + h*0.15:.1f}" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.5"/>')
    else:
        o.append(f'<path d="{"M%.1f,%.1f " % (xin, yin)}{lower}" stroke="{linea}" stroke-width="1.4" fill="none" opacity="0.45"/>')
    if viejo:
        o.append(f'<path d="M{cx - w*0.4:.1f},{cy + h*1.15:.1f} Q{cx:.1f},{cy + h*1.7:.1f} {cx + w*0.4:.1f},{cy + h*1.15:.1f}" stroke="{linea}" stroke-width="1.5" fill="none" opacity="0.4"/>')
        for k in range(3):
            o.append(f'<path d="M{xout + lado*-1*-4:.1f},{yout - 4 + k*6:.1f} l{lado*-1*-14:.1f},{-4 + k*4:.1f}" stroke="{linea}" stroke-width="1.3" opacity="0.35"/>')
    return "".join(o)


def ceja(cx, cy, w, estado, lado, color, grosor=5.0):
    xin = cx + (w / 2 if lado < 0 else -w / 2)
    xout = cx - (w / 2 if lado < 0 else -w / 2)
    if estado == "triste":
        yin, yout, ctrl = cy - 7, cy + 2, cy - 6
    elif estado == "sonrisa":
        yin, yout, ctrl = cy + 1, cy + 3, cy - 8
    elif estado == "ceño":
        yin, yout, ctrl = cy + 6, cy - 3, cy - 4
    else:
        yin, yout, ctrl = cy + 2, cy + 3, cy - 7
    return (f'<path d="M{xin:.1f},{yin:.1f} Q{cx:.1f},{ctrl:.1f} {xout:.1f},{yout:.1f}" stroke="{color}" stroke-width="{grosor}" '
            f'fill="none" stroke-linecap="round"/>')


def boca(cx, cy, w, estado, labio="#a9545c", linea=LINE, labios=True):
    o = []
    if estado == "sonrisa":
        o.append(f'<path d="M{cx-w/2:.1f},{cy-2:.1f} Q{cx:.1f},{cy+11:.1f} {cx+w/2:.1f},{cy-2:.1f}" stroke="{linea}" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
        if labios:
            o.append(f'<path d="M{cx-w*0.35:.1f},{cy+5:.1f} Q{cx:.1f},{cy+15:.1f} {cx+w*0.35:.1f},{cy+5:.1f} Q{cx:.1f},{cy+9:.1f} {cx-w*0.35:.1f},{cy+5:.1f} Z" fill="{labio}" opacity="0.85"/>')
    elif estado == "triste":
        o.append(f'<path d="M{cx-w/2:.1f},{cy+4:.1f} Q{cx:.1f},{cy-3:.1f} {cx+w/2:.1f},{cy+4:.1f}" stroke="{linea}" stroke-width="2.4" fill="none" stroke-linecap="round"/>')
        if labios:
            o.append(f'<path d="M{cx-w*0.35:.1f},{cy+4:.1f} Q{cx:.1f},{cy+14:.1f} {cx+w*0.35:.1f},{cy+4:.1f} Q{cx:.1f},{cy+2:.1f} {cx-w*0.35:.1f},{cy+4:.1f} Z" fill="{labio}" opacity="0.8"/>')
    else:
        if labios:
            o.append(f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx-w*0.25:.1f},{cy-7:.1f} {cx:.1f},{cy-4:.1f} Q{cx+w*0.25:.1f},{cy-7:.1f} {cx+w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+2:.1f} {cx-w/2:.1f},{cy:.1f} Z" fill="{labio}" opacity="0.9"/>')
            o.append(f'<path d="M{cx-w*0.42:.1f},{cy+1:.1f} Q{cx:.1f},{cy+15:.1f} {cx+w*0.42:.1f},{cy+1:.1f} Q{cx:.1f},{cy+4:.1f} {cx-w*0.42:.1f},{cy+1:.1f} Z" fill="{labio}"/>')
            o.append(f'<path d="M{cx-w*0.15:.1f},{cy+7:.1f} Q{cx:.1f},{cy+9:.1f} {cx+w*0.15:.1f},{cy+7:.1f}" stroke="#ffffff" stroke-width="2" opacity="0.35" fill="none"/>')
        o.append(f'<path d="M{cx-w/2:.1f},{cy:.1f} Q{cx:.1f},{cy+3:.1f} {cx+w/2:.1f},{cy:.1f}" stroke="{linea}" stroke-width="2.2" fill="none" stroke-linecap="round"/>')
    return "".join(o)


def paloma(x, y, s=1.0, color="#d9dee5", sombra="#6f7885"):
    """Prendedor: palomita de plata con las alas abiertas."""
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M-2,0 C-10,-14 -26,-18 -34,-10 C-24,-8 -16,-2 -10,4 Z" fill="{color}" stroke="{sombra}" stroke-width="1.5"/>'
            f'<path d="M2,0 C10,-16 26,-22 36,-14 C26,-10 18,-3 12,4 Z" fill="{color}" stroke="{sombra}" stroke-width="1.5"/>'
            f'<ellipse cx="0" cy="6" rx="13" ry="7" fill="{color}" stroke="{sombra}" stroke-width="1.5"/>'
            f'<circle cx="11" cy="1" r="5" fill="{color}" stroke="{sombra}" stroke-width="1.5"/>'
            f'<path d="M15,1 l5,1 -5,2 Z" fill="#c9a24a"/>'
            f'<path d="M-12,6 L-24,2 L-22,12 Z" fill="{color}" stroke="{sombra}" stroke-width="1.5"/>'
            f'<circle cx="12" cy="0" r="1.2" fill="#222"/>'
            f'<path d="M-6,-2 C-12,-10 -20,-12 -26,-10" stroke="{sombra}" stroke-width="1" fill="none"/>'
            f'</g>')


def tejido_pattern(pid, base, linea, paso=9):
    return (f'<pattern id="{pid}" width="{paso}" height="14" patternUnits="userSpaceOnUse">'
            f'<rect width="{paso}" height="14" fill="{base}"/>'
            f'<path d="M0,0 L{paso/2},6 L{paso},0 M0,7 L{paso/2},13 L{paso},7" stroke="{linea}" stroke-width="1.6" fill="none" opacity="0.55"/>'
            f'</pattern>')


# ---------------------------------------------------------------------------
#  INÉS
# ---------------------------------------------------------------------------

PIEL_I = "#efe4dc"
PIEL_I_S = "#b9aab4"
PELO_I = "#141118"
ROJO = "#a3192d"
ROJO_S = "#5c0c1a"
ROJO_L = "#c8323f"


def ines(estado="neutral", chaqueta=True, out=None, efecto=True):
    cx = 410
    defs = tejido_pattern("lana", ROJO, ROJO_S) + tejido_pattern("lanaS", ROJO_S, "#33060f") + \
        ('<linearGradient id="vestido" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#f3eee4"/><stop offset="1" stop-color="#b8b6c2"/></linearGradient>')
    b = []
    # ---- pelo de atrás (con las puntas hacia afuera, peinado de los sesenta)
    b.append(f'<path d="M300,330 C288,190 340,118 412,116 C488,116 538,186 524,330 C520,392 538,450 584,476 '
             f'C548,500 508,492 486,466 L338,466 C314,492 274,500 238,476 C284,450 304,392 300,330 Z" fill="{PELO_I}"/>')
    # ---- cuello
    b.append(f'<path d="M372,436 L364,548 L458,548 L450,436 Z" fill="{PIEL_I}"/>')
    b.append(f'<path d="M372,450 Q412,500 450,450 L452,500 Q412,522 370,500 Z" fill="{PIEL_I_S}" opacity="0.65"/>')
    # ---- cuerpo
    b.append('<g transform="translate(0,-40)">')
    if chaqueta:
        # vestido visible en la abertura
        b.append('<path d="M330,540 L490,540 L470,1130 L350,1130 Z" fill="url(#vestido)"/>')
        # cuello Peter Pan
        b.append(f'<path d="M411,552 C380,544 350,552 344,570 C360,594 396,588 411,566 Z" fill="#fbf8f2" stroke="{LINE}" stroke-width="2"/>')
        b.append(f'<path d="M411,552 C442,544 472,552 478,570 C462,594 426,588 411,566 Z" fill="#e6e3ea" stroke="{LINE}" stroke-width="2"/>')
        # chaqueta: cuerpo y mangas (enorme, de hombre)
        b.append(f'<path d="M352,540 C300,548 210,566 170,600 C130,636 118,700 112,780 L96,1130 L398,1130 L392,860 C372,760 352,650 352,540 Z" fill="url(#lana)"/>')
        b.append(f'<path d="M470,540 C522,548 612,566 652,600 C692,636 704,700 710,780 L726,1130 L424,1130 L430,860 C450,760 470,650 470,540 Z" fill="url(#lanaS)"/>')
        # luz cálida sobre el lado izquierdo
        b.append(f'<path d="M170,600 C130,636 118,700 112,780 L104,1130 L170,1130 C170,900 180,720 230,610 Z" fill="{ROJO_L}" opacity="0.55"/>')
        # costuras de manga
        b.append(f'<path d="M232,610 C214,700 214,860 222,1130" stroke="{ROJO_S}" stroke-width="4" fill="none" opacity="0.8"/>')
        b.append(f'<path d="M590,610 C608,700 608,860 600,1130" stroke="#2a0509" stroke-width="4" fill="none" opacity="0.8"/>')
        # puños gruesos que tapan las manos (abajo)
        b.append(f'<path d="M150,1000 L270,1000 L272,1130 L146,1130 Z" fill="{ROJO_S}" opacity="0.55"/>')
        b.append(f'<path d="M552,1000 L672,1000 L676,1130 L548,1130 Z" fill="#33060f" opacity="0.6"/>')
        # solapas (cuello chal)
        b.append(f'<path d="M352,540 C336,620 340,740 392,860 L404,860 C368,740 366,630 380,548 Z" fill="{ROJO_S}"/>')
        b.append(f'<path d="M470,540 C486,620 482,740 430,860 L418,860 C454,740 456,630 442,548 Z" fill="#3c0711"/>')
        b.append(f'<path d="M352,540 C336,620 340,740 392,860" stroke="{LINE}" stroke-width="3" fill="none"/>')
        b.append(f'<path d="M470,540 C486,620 482,740 430,860" stroke="{LINE}" stroke-width="3" fill="none"/>')
        # botones
        for y in (700, 820, 940):
            b.append(f'<circle cx="{442 + (y-700)*-0.06:.0f}" cy="{y}" r="11" fill="#3a2418" stroke="{LINE}" stroke-width="2"/>'
                     f'<circle cx="{439 + (y-700)*-0.06:.0f}" cy="{y-3}" r="3" fill="#7a5a44"/>')
        # contorno
        b.append(f'<path d="M352,540 C300,548 210,566 170,600 C130,636 118,700 112,780 L96,1130" stroke="{LINE}" stroke-width="4" fill="none"/>')
        b.append(f'<path d="M470,540 C522,548 612,566 652,600 C692,636 704,700 710,780 L726,1130" stroke="{LINE}" stroke-width="4" fill="none"/>')
        # palomita de plata en la solapa
        b.append(paloma(366, 640, 0.75))
    else:
        # sin chaqueta: vestido claro con manga tres cuartos y brazos cruzados por el frío
        b.append(f'<path d="M372,548 C320,556 262,572 236,604 C214,640 214,700 224,760 L254,1130 L566,1130 L596,760 '
                 f'C606,700 606,640 584,604 C558,572 500,556 448,548 Z" fill="url(#vestido)" stroke="{LINE}" stroke-width="4"/>')
        b.append(f'<path d="M411,552 C380,544 350,552 344,570 C360,594 396,588 411,566 Z" fill="#fbf8f2" stroke="{LINE}" stroke-width="2"/>')
        b.append(f'<path d="M411,552 C442,544 472,552 478,570 C462,594 426,588 411,566 Z" fill="#e6e3ea" stroke="{LINE}" stroke-width="2"/>')
        # pinzas del vestido
        b.append(f'<path d="M330,700 Q340,820 330,900 M492,700 Q482,820 492,900" stroke="#9b97a6" stroke-width="2" fill="none" opacity="0.6"/>')
        # brazos: superiores por los costados, manos juntas contra el pecho
        b.append(f'<path d="M238,610 C214,690 214,780 232,860 L300,856 C292,780 294,700 304,626 Z" fill="#ece8e2" stroke="{LINE}" stroke-width="3"/>')
        b.append(f'<path d="M582,610 C606,690 606,780 588,860 L520,856 C528,780 526,700 516,626 Z" fill="#c3c0cb" stroke="{LINE}" stroke-width="3"/>')
        # antebrazos subiendo hacia el centro
        b.append(f'<path d="M236,842 C290,800 340,770 386,742 L408,778 C366,808 318,842 296,868 Z" fill="{PIEL_I}" stroke="{LINE}" stroke-width="3"/>')
        b.append(f'<path d="M584,842 C530,800 480,770 436,742 L414,778 C456,808 502,842 526,868 Z" fill="{PIEL_I_S}" stroke="{LINE}" stroke-width="3"/>')
        # puños de manga tres cuartos
        b.append(f'<path d="M226,836 L302,846 L298,884 L232,874 Z" fill="#f4f0ea" stroke="{LINE}" stroke-width="3"/>')
        b.append(f'<path d="M594,836 L518,846 L522,884 L588,874 Z" fill="#cfccd6" stroke="{LINE}" stroke-width="3"/>')
        # manos entrelazadas
        b.append(f'<path d="M384,730 C392,708 430,704 440,722 C448,740 436,768 410,772 C390,772 378,752 384,730 Z" fill="{PIEL_I}" stroke="{LINE}" stroke-width="3"/>')
        b.append(f'<path d="M396,724 L402,760 M410,720 L414,762 M424,722 L426,758" stroke="{PIEL_I_S}" stroke-width="2.5" fill="none" opacity="0.9"/>')
    b.append('</g>')
    # ---- cara
    face = f"M324,296 C324,220 498,220 498,296 C500,372 474,434 411,468 C348,434 322,372 324,296 Z"
    b.append(f'<path d="{face}" fill="{PIEL_I}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M498,300 C500,372 474,434 411,468 C452,428 472,372 478,300 Z" fill="{PIEL_I_S}" opacity="0.5"/>')
    b.append(f'<ellipse cx="362" cy="392" rx="22" ry="12" fill="#e59a9a" opacity="0.18"/><ellipse cx="460" cy="392" rx="22" ry="12" fill="#e59a9a" opacity="0.14"/>')
    # ojos y cejas
    b.append(ceja(370, 306, 52, estado, -1, PELO_I, 5))
    b.append(ceja(452, 306, 52, estado, 1, PELO_I, 5))
    b.append(ojo(370, 340, 50, 14, estado, -1, iris="#3a2620", piel_sombra=PIEL_I_S))
    b.append(ojo(452, 340, 50, 14, estado, 1, iris="#3a2620", piel_sombra=PIEL_I_S))
    # nariz
    b.append(f'<path d="M414,344 Q422,372 414,384" stroke="{PIEL_I_S}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M401,388 Q411,394 421,388" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.55" stroke-linecap="round"/>')
    # boca
    b.append(boca(411, 418, 38, estado, labio="#b0525c"))
    # ---- pelo de adelante: volumen, flequillo y mechones
    b.append(f'<path d="M318,262 C300,160 356,98 414,98 C478,98 530,156 508,262 C492,226 470,214 440,212 C400,210 352,222 318,262 Z" fill="{PELO_I}"/>')
    b.append(f'<path d="M322,282 C328,232 380,206 452,208 C484,210 506,228 510,258 C488,244 452,240 424,252 C398,262 382,278 372,296 C358,284 340,280 322,282 Z" fill="{PELO_I}"/>')
    b.append(f'<path d="M330,276 C320,340 324,404 350,456 C330,446 312,404 308,334 C306,300 314,284 330,276 Z" fill="{PELO_I}"/>')
    b.append(f'<path d="M494,270 C504,340 500,404 474,456 C494,446 512,404 516,334 C518,300 510,284 494,270 Z" fill="{PELO_I}"/>')
    # brillos azulados
    for d in ["M344,180 C366,128 430,112 470,140", "M352,210 C380,160 440,150 486,182", "M360,246 C400,226 450,226 490,246",
              "M296,360 C292,420 270,460 248,474", "M528,360 C532,420 556,456 578,470"]:
        b.append(f'<path d="{d}" stroke="#4a5a7a" stroke-width="3" fill="none" opacity="0.55" stroke-linecap="round"/>')
    # cintillo blanco
    b.append(f'<path d="M318,236 C352,170 470,164 510,232" stroke="#efe9df" stroke-width="10" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M318,236 C352,170 470,164 510,232" stroke="{LINE}" stroke-width="1.5" fill="none" opacity="0.4" transform="translate(0,6)"/>')
    # contornos de pelo
    b.append(f'<path d="M300,330 C288,190 340,118 412,116 C488,116 538,186 524,330 C520,392 538,450 584,476" stroke="{LINE}" stroke-width="3" fill="none" opacity="0.7"/>')
    name = f"ines_{'sin' if not chaqueta else estado}.png"
    p = out or f"{SP}/{name}"
    render(sdoc("".join(b), defs), p)
    if efecto:
        post_sprite(p, ghost=True, fade_bottom=True, glow=True, grain=3)
    return p


if __name__ == "__main__":
    for e in ("neutral", "triste", "sonrisa"):
        ines(e)
    ines("neutral", chaqueta=False)
    print("ok")


# ---------------------------------------------------------------------------
#  HOMBRES
# ---------------------------------------------------------------------------

def orejas(xl, xr, y, piel, sombra, ry=30):
    return (f'<ellipse cx="{xl}" cy="{y}" rx="16" ry="{ry}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>'
            f'<path d="M{xl+2},{y-14} Q{xl-8},{y} {xl+2},{y+14}" stroke="{sombra}" stroke-width="3" fill="none"/>'
            f'<ellipse cx="{xr}" cy="{y}" rx="16" ry="{ry}" fill="{sombra}" stroke="{LINE}" stroke-width="3"/>'
            f'<path d="M{xr-2},{y-14} Q{xr+8},{y} {xr-2},{y+14}" stroke="#5a4038" stroke-width="3" fill="none"/>')


def anteojos(xl, xr, y, r=33, color="#9a8a6a"):
    return (f'<circle cx="{xl}" cy="{y}" r="{r}" fill="#cfe3ff" fill-opacity="0.06" stroke="{color}" stroke-width="3.5"/>'
            f'<circle cx="{xr}" cy="{y}" r="{r}" fill="#cfe3ff" fill-opacity="0.06" stroke="{color}" stroke-width="3.5"/>'
            f'<path d="M{xl+r},{y-4} Q{(xl+xr)/2},{y-14} {xr-r},{y-4}" stroke="{color}" stroke-width="3" fill="none"/>'
            f'<path d="M{xl-r},{y-6} L{xl-r-28},{y-10}" stroke="{color}" stroke-width="3"/>'
            f'<path d="M{xr+r},{y-6} L{xr+r+28},{y-10}" stroke="{color}" stroke-width="3"/>'
            f'<path d="M{xl-18},{y+14} L{xl+6},{y-20}" stroke="#ffffff" stroke-width="4" opacity="0.22"/>'
            f'<path d="M{xr-18},{y+14} L{xr+6},{y-20}" stroke="#ffffff" stroke-width="4" opacity="0.22"/>')


def tomas_viejo(estado="neutral"):
    piel, som = "#dcbca4", "#a07f74"
    pelo, pelo_s = "#e6e3de", "#a9a6a2"
    b = []
    defs = tejido_pattern("cardigan", "#5b4a3b", "#3e3127", paso=8)
    # cuerpo: camisa y chaleco de lana (hombros caídos)
    b.append(f'<path d="M372,440 L366,560 L456,560 L450,440 Z" fill="{piel}"/>')
    b.append(f'<path d="M372,456 Q412,496 450,456 L452,520 Q412,540 370,520 Z" fill="{som}" opacity="0.7"/>')
    b.append(f'<path d="M398,470 L404,540 M424,470 L418,540" stroke="{som}" stroke-width="3" opacity="0.8"/>')
    b.append(f'<path d="M352,540 C290,556 220,580 186,620 C150,664 140,760 136,860 L128,1080 L694,1080 L686,860 C682,760 672,664 636,620 C602,580 532,556 470,540 Z" fill="url(#cardigan)" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M636,620 C672,664 682,760 686,860 L694,1080 L560,1080 C580,880 590,700 560,600 Z" fill="#2c231c" opacity="0.6"/>')
    # camisa (cuello en V del chaleco)
    b.append(f'<path d="M356,540 L411,700 L466,540 Z" fill="#e9e5dc" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M356,540 L384,600 L411,566 Z" fill="#f6f3ec" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M466,540 L438,600 L411,566 Z" fill="#cfcbc3" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M350,540 L411,720 L472,540" stroke="#3e3127" stroke-width="16" fill="none"/>')
    for y in (760, 860, 960):
        b.append(f'<circle cx="411" cy="{y}" r="9" fill="#2a1f17" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<path d="M411,720 L411,1080" stroke="{LINE}" stroke-width="3"/>')
    # bolsillo de camisa / carta (se insinúa)
    b.append('<g transform="translate(411 480) scale(1.2) translate(-411 -480)">')
    # orejas y cara
    b.append(orejas(326, 496, 344, piel, som))
    face = "M330,300 C328,212 494,212 492,300 C494,384 466,444 411,474 C356,444 328,384 330,300 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M492,300 C494,384 466,444 411,474 C452,430 472,380 474,300 Z" fill="{som}" opacity="0.5"/>')
    # mejillas hundidas y surcos
    b.append(f'<path d="M352,380 Q358,420 380,444" stroke="{som}" stroke-width="3" fill="none" opacity="0.7"/>')
    b.append(f'<path d="M470,380 Q464,420 442,444" stroke="{som}" stroke-width="3" fill="none" opacity="0.7"/>')
    b.append(f'<path d="M392,392 Q378,410 384,436" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.45"/>')
    b.append(f'<path d="M430,392 Q444,410 438,436" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.45"/>')
    # arrugas de la frente
    for k, y in enumerate((252, 266, 280)):
        b.append(f'<path d="M{368+k*4},{y} Q411,{y-8} {454-k*4},{y}" stroke="{som}" stroke-width="2.2" fill="none" opacity="0.8"/>')
    # cejas canosas y ojos
    b.append(ceja(372, 308, 50, estado, -1, "#cfcac2", 7))
    b.append(ceja(450, 308, 50, estado, 1, "#cfcac2", 7))
    hum = estado == "triste"
    b.append(ojo(372, 340, 40, 10, estado if estado != "sonrisa" else "neutral", -1, iris="#4a3a2c", pest=3, viejo=True, humedo=hum, piel_sombra=som))
    b.append(ojo(450, 340, 40, 10, estado if estado != "sonrisa" else "neutral", 1, iris="#4a3a2c", pest=3, viejo=True, humedo=hum, piel_sombra=som))
    if hum:
        b.append(f'<path d="M462,356 Q466,380 462,402" stroke="#dff0ff" stroke-width="3" fill="none" opacity="0.7"/>')
    # nariz
    b.append(f'<path d="M414,336 Q424,384 418,398" stroke="{som}" stroke-width="3.5" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M398,400 Q411,410 426,400" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    # boca
    b.append(boca(411, 432, 42, estado, labio="#b07a72", labios=False))
    b.append(f'<path d="M398,452 Q411,458 424,452" stroke="{som}" stroke-width="2" fill="none" opacity="0.7"/>')
    # pelo blanco: costados y atrás, peinado hacia atrás y escaso arriba
    b.append(f'<path d="M330,300 C322,250 330,222 352,206 C340,240 342,272 346,300 Z" fill="{pelo}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<path d="M492,300 C500,250 492,222 470,206 C482,240 480,272 476,300 Z" fill="{pelo_s}" stroke="{LINE}" stroke-width="2"/>')
    b.append(f'<path d="M340,236 C350,196 384,178 414,178 C446,178 472,196 482,236 C462,214 440,206 412,206 C384,206 360,214 340,236 Z" fill="{pelo}" opacity="0.85"/>')
    for k in range(6):
        b.append(f'<path d="M{356+k*20},{222-abs(k-2.5)*3:.0f} Q{376+k*16},{190} {430+k*6},{184+abs(k-2.5)*2:.0f}" stroke="{pelo_s}" stroke-width="2" fill="none" opacity="0.7"/>')
    b.append(f'<path d="M346,212 C380,186 444,184 476,210" stroke="{pelo_s}" stroke-width="2" fill="none"/>')
    # anteojos
    b.append(anteojos(372, 450, 342))
    b.append('</g>')
    p = f"{SP}/tomas_{estado}.png"
    render(sdoc("".join(b), defs), p)
    post_sprite(p, grain=3)
    return p


def lucho(estado="neutral"):
    piel, som = "#c99a78", "#8a6052"
    b = []
    defs = ('<pattern id="tweed" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#3b3e45"/>'
            '<path d="M0,10 L10,0 M-2,2 L2,-2 M8,12 L12,8" stroke="#2a2c31" stroke-width="2"/></pattern>')
    # chaqueta de cuero y bufanda
    b.append(f'<path d="M368,446 L360,560 L462,560 L454,446 Z" fill="{piel}"/>')
    b.append(f'<path d="M346,532 C280,548 200,576 160,620 C120,666 110,770 106,870 L96,1080 L726,1080 L716,870 C712,770 702,666 662,620 C622,576 542,548 476,532 Z" fill="#1d2532" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M662,620 C702,666 712,770 716,870 L726,1080 L590,1080 C600,880 610,700 590,600 Z" fill="#0f141c" opacity="0.7"/>')
    b.append(f'<path d="M160,620 C120,666 110,770 106,870 L100,1000 C140,860 150,720 200,612 Z" fill="#4a5a76" opacity="0.35"/>')
    # solapas
    b.append(f'<path d="M346,540 L300,640 L380,700 L411,600 Z" fill="#151b25" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M476,540 L522,640 L442,700 L411,600 Z" fill="#0c1018" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M411,700 L411,1080" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M418,720 L418,1080" stroke="#8b8f96" stroke-width="2" stroke-dasharray="6 6" opacity="0.6"/>')
    # bufanda
    b.append(f'<path d="M352,520 C380,560 444,560 472,520 L486,560 C450,600 372,600 338,560 Z" fill="#8a6a2a" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M430,580 L452,700 L420,712 L408,590 Z" fill="#7a5c22" stroke="{LINE}" stroke-width="3"/>')
    for k in range(4):
        b.append(f'<path d="M{352+k*30},{534+k*4} l10,30" stroke="#5e4618" stroke-width="2" opacity="0.6"/>')
    b.append('<g transform="translate(411 480) scale(1.2) translate(-411 -480)">')
    # cara redonda
    b.append(orejas(316, 506, 336, piel, som))
    face = "M318,300 C318,206 504,206 504,300 C508,386 478,448 411,478 C344,448 314,386 318,300 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M504,300 C508,386 478,448 411,478 C460,430 484,380 486,300 Z" fill="{som}" opacity="0.5"/>')
    # papada y surcos
    b.append(f'<path d="M360,440 Q411,470 462,440" stroke="{som}" stroke-width="3" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M378,386 Q360,410 370,440" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.5"/>')
    b.append(f'<path d="M444,386 Q462,410 452,440" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.5"/>')
    # cicatriz (de la oreja a la comisura)
    b.append(f'<path d="M494,336 Q480,380 450,418" stroke="#e6b8a8" stroke-width="5" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M494,336 Q480,380 450,418" stroke="#8a4a42" stroke-width="2" fill="none" stroke-linecap="round" transform="translate(2,1)"/>')
    for t in (0.2, 0.45, 0.7):
        x = 494 + (450 - 494) * t
        y = 336 + (418 - 336) * t
        b.append(f'<path d="M{x-6:.0f},{y-4:.0f} l12,6" stroke="#8a4a42" stroke-width="1.8" opacity="0.7"/>')
    # cejas pobladas canosas, ojos chicos con párpado pesado
    eb = "triste" if estado == "triste" else "ceño"
    b.append(ceja(368, 306, 54, eb, -1, "#d8d4cc", 9))
    b.append(ceja(454, 306, 54, eb, 1, "#d8d4cc", 9))
    eo = "triste" if estado == "triste" else "neutral"
    b.append(ojo(368, 336, 38, 9, eo, -1, iris="#2a1e18", pest=3.5, viejo=True, humedo=(estado == "triste"), piel_sombra=som))
    b.append(ojo(454, 336, 38, 9, eo, 1, iris="#2a1e18", pest=3.5, viejo=True, humedo=(estado == "triste"), piel_sombra=som))
    b.append(f'<path d="M346,326 Q368,316 390,326" stroke="{som}" stroke-width="4" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M432,326 Q454,316 476,326" stroke="{som}" stroke-width="4" fill="none" opacity="0.6"/>')
    # nariz ancha
    b.append(f'<path d="M412,336 Q426,376 418,392" stroke="{som}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M392,394 Q411,408 432,394" stroke="{LINE}" stroke-width="2.6" fill="none" opacity="0.6"/>')
    # bigote blanco
    b.append(f'<path d="M362,412 C374,396 404,398 411,406 C420,398 448,396 460,412 C454,432 430,428 411,420 C392,428 368,432 362,412 Z" fill="#ebe8e2" stroke="{LINE}" stroke-width="2.5"/>')
    for k in range(7):
        b.append(f'<path d="M{372+k*13},{408} l{2},{12}" stroke="#b9b4ab" stroke-width="2"/>')
    # labio inferior
    if estado == "triste":
        b.append(f'<path d="M392,440 Q411,434 430,440" stroke="{LINE}" stroke-width="2.4" fill="none"/>')
    else:
        b.append(f'<path d="M394,436 Q411,442 428,436" stroke="{LINE}" stroke-width="2.4" fill="none"/>')
    # gorra (jockey de lana)
    b.append(f'<path d="M300,272 C294,176 352,140 418,140 C494,140 534,186 526,262 C470,244 360,246 300,272 Z" fill="url(#tweed)" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M314,262 C352,232 476,228 516,254 C512,282 460,280 411,278 C364,280 318,286 314,262 Z" fill="#2c2f35" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M300,272 C360,246 470,244 526,262" stroke="#55585f" stroke-width="2" fill="none"/>')
    b.append(f'<circle cx="418" cy="146" r="6" fill="#2c2f35"/>')
    # canas bajo la gorra
    b.append(f'<path d="M306,282 C300,300 304,320 312,330 L322,300 Z" fill="#e3e0da"/>')
    b.append(f'<path d="M516,282 C522,300 518,320 510,330 L500,300 Z" fill="#b9b5ad"/>')
    b.append('</g>')
    p = f"{SP}/lucho_{estado}.png"
    render(sdoc("".join(b), defs), p)
    post_sprite(p, grain=3)
    return p


def arsenio():
    piel, som = "#a87a5c", "#6e4c3e"
    b = []
    defs = ('<pattern id="poncho" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#6a4a32"/>'
            '<path d="M0,20 L40,20" stroke="#5a3d28" stroke-width="3"/></pattern>'
            '<radialGradient id="linterna" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff6d8" stop-opacity="0.9"/><stop offset="1" stop-color="#fff6d8" stop-opacity="0"/></radialGradient>')
    b.append(f'<path d="M370,446 L362,560 L460,560 L452,446 Z" fill="{piel}"/>')
    # poncho
    b.append(f'<path d="M362,520 L460,520 C560,560 690,640 760,760 L790,1080 L30,1080 L60,760 C130,640 262,560 362,520 Z" fill="url(#poncho)" stroke="{LINE}" stroke-width="4"/>')
    defs += '<clipPath id="ponchoC"><path d="M362,520 L460,520 C560,560 690,640 760,760 L790,1080 L30,1080 L60,760 C130,640 262,560 362,520 Z"/></clipPath>'
    fr = []
    for k, (y, col) in enumerate(((700, "#a3743f"), (730, "#2f2016"), (900, "#a3743f"), (940, "#c9a46a"), (970, "#2f2016"))):
        fr.append(f'<path d="M0,{y} Q411,{y-60} 820,{y}" stroke="{col}" stroke-width="{14 if k%2==0 else 8}" fill="none" opacity="0.9"/>')
    b.append('<g clip-path="url(#ponchoC)">' + "".join(fr) + '</g>')
    b.append(f'<path d="M460,520 C560,560 690,640 760,760 L790,1080 L520,1080 C560,860 540,680 460,560 Z" fill="#1d130c" opacity="0.45"/>')
    # cuello del poncho
    b.append(f'<path d="M350,520 Q411,560 472,520 L478,548 Q411,590 344,548 Z" fill="#4a3322" stroke="{LINE}" stroke-width="3"/>')
    # mano con linterna
    b.append(f'<path d="M520,860 C540,830 590,830 600,860 C606,890 580,910 548,906 C526,902 514,884 520,860 Z" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<g transform="rotate(32 560 860)"><rect x="530" y="800" width="58" height="120" rx="8" fill="#2a2c30" stroke="{LINE}" stroke-width="3"/>'
             f'<rect x="522" y="910" width="74" height="30" rx="6" fill="#3a3d42" stroke="{LINE}" stroke-width="3"/>'
             f'<ellipse cx="559" cy="944" rx="34" ry="8" fill="#fff6d8"/></g>')
    b.append(f'<circle cx="520" cy="935" r="110" fill="url(#linterna)" opacity="0.7"/>')
    b.append('<g transform="translate(411 480) scale(1.2) translate(-411 -480)">')
    # cara cuadrada curtida
    b.append(orejas(318, 504, 340, piel, som, ry=28))
    face = "M320,290 C320,212 502,212 502,290 C504,360 490,430 448,462 L374,462 C332,430 318,360 320,290 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M502,290 C504,360 490,430 448,462 L430,462 C470,420 486,360 484,290 Z" fill="{som}" opacity="0.55"/>')
    # barba de días
    rnd = random.Random(5)
    for _ in range(260):
        x = rnd.uniform(340, 482)
        y = rnd.uniform(400, 462)
        if (x - 411) ** 2 / 75 ** 2 + (y - 400) ** 2 / 70 ** 2 < 1.1 and not (390 < x < 432 and 404 < y < 432):
            b.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="1.3" fill="#3a2a22" opacity="0.6"/>')
    # ojos hundidos con sombra
    b.append(f'<ellipse cx="370" cy="330" rx="34" ry="16" fill="{som}" opacity="0.28"/><ellipse cx="452" cy="330" rx="34" ry="16" fill="{som}" opacity="0.32"/>')
    b.append(ceja(370, 306, 54, "ceño", -1, "#2a221e", 9))
    b.append(ceja(452, 306, 54, "ceño", 1, "#2a221e", 9))
    b.append(ojo(370, 336, 36, 8, "neutral", -1, iris="#1e1410", pest=3.5, viejo=True, piel_sombra=som))
    b.append(ojo(452, 336, 36, 8, "neutral", 1, iris="#1e1410", pest=3.5, viejo=True, piel_sombra=som))
    # nariz y bigote canoso
    b.append(f'<path d="M412,336 Q424,374 416,392" stroke="{som}" stroke-width="4" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M394,394 Q411,404 430,394" stroke="{LINE}" stroke-width="2.4" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M380,414 C392,404 404,406 411,410 C418,406 430,404 442,414 C432,422 420,420 411,418 C402,420 390,422 380,414 Z" fill="#5b5550"/>')
    b.append(f'<path d="M392,434 Q411,438 430,434" stroke="{LINE}" stroke-width="2.4" fill="none"/>')
    b.append(f'<path d="M378,252 Q411,244 444,252" stroke="{som}" stroke-width="2.5" fill="none" opacity="0.7"/>')
    # gorro de lana
    b.append(f'<path d="M306,282 C300,170 356,128 414,128 C476,128 528,172 518,282 Z" fill="#2f3d33" stroke="{LINE}" stroke-width="3"/>')
    for k in range(14):
        x = 318 + k * 15
        b.append(f'<path d="M{x},{280} Q{x+3},{200} {x+8 if k<7 else x-2},{150 + abs(k-7)*4}" stroke="#24302a" stroke-width="3" fill="none"/>')
    b.append(f'<path d="M302,250 C350,236 470,234 522,250 L522,288 C470,272 350,274 302,288 Z" fill="#3a4a3f" stroke="{LINE}" stroke-width="3"/>')
    for k in range(16):
        x = 308 + k * 13.5
        b.append(f'<line x1="{x:.0f}" y1="250" x2="{x:.0f}" y2="286" stroke="#2b372f" stroke-width="2.5"/>')
    b.append('</g>')
    p = f"{SP}/arsenio_neutral.png"
    render(sdoc("".join(b), defs), p)
    post_sprite(p, grain=3)
    return p


def tomas_joven(path, chaqueta=True):
    """Tomás a los veinte (para la foto y el recuerdo). Se guarda fuera de sprites."""
    piel, som = "#e2c2a6", "#a8857a"
    pelo = "#16110f"
    b = []
    defs = tejido_pattern("lanaJ", ROJO, ROJO_S)
    b.append(f'<path d="M376,440 L370,560 L452,560 L446,440 Z" fill="{piel}"/>')
    b.append(f'<path d="M376,456 Q411,496 446,456 L448,520 Q411,540 374,520 Z" fill="{som}" opacity="0.6"/>')
    b.append(f'<path d="M350,536 C290,550 220,572 186,612 C150,656 140,760 136,860 L128,1080 L694,1080 L686,860 C682,760 672,656 636,612 C602,572 532,550 472,536 Z" fill="{'url(#lanaJ)' if chaqueta else '#2c2c34'}" stroke="{LINE}" stroke-width="4"/>')
    b.append(f'<path d="M356,536 L411,690 L466,536 Z" fill="#f2efe8" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M356,536 L388,610 L411,562 Z" fill="#ffffff" stroke="{LINE}" stroke-width="2.5"/>')
    b.append(f'<path d="M466,536 L434,610 L411,562 Z" fill="#dedad2" stroke="{LINE}" stroke-width="2.5"/>')
    if chaqueta:
        b.append(f'<path d="M350,536 C334,620 340,720 396,840 L408,840 C366,720 364,630 378,546 Z" fill="{ROJO_S}"/>')
        b.append(f'<path d="M472,536 C488,620 482,720 426,840 L414,840 C456,720 458,630 444,546 Z" fill="#3c0711"/>')
        b.append(paloma(368, 640, 0.75))
    b.append('<g transform="translate(411 480) scale(1.2) translate(-411 -480)">')
    b.append(orejas(328, 494, 344, piel, som, ry=28))
    face = "M330,296 C330,218 492,218 492,296 C494,372 468,432 411,462 C354,432 328,372 330,296 Z"
    b.append(f'<path d="{face}" fill="{piel}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M492,300 C494,372 468,432 411,462 C452,424 470,372 474,300 Z" fill="{som}" opacity="0.45"/>')
    b.append(ceja(372, 306, 50, "neutral", -1, pelo, 6))
    b.append(ceja(450, 306, 50, "neutral", 1, pelo, 6))
    b.append(ojo(372, 338, 42, 11, "sonrisa", -1, iris="#3a2a20", pest=3.5, piel_sombra=som))
    b.append(ojo(450, 338, 42, 11, "sonrisa", 1, iris="#3a2a20", pest=3.5, piel_sombra=som))
    b.append(f'<path d="M414,340 Q422,372 414,386" stroke="{som}" stroke-width="3" fill="none" stroke-linecap="round"/>')
    b.append(f'<path d="M400,390 Q411,396 422,390" stroke="{LINE}" stroke-width="2" fill="none" opacity="0.55"/>')
    b.append(boca(411, 416, 46, "sonrisa", labio="#b07068"))
    # pelo engominado con jopo
    b.append(f'<path d="M328,300 C318,226 336,166 398,150 C452,138 504,166 502,232 C502,256 498,276 494,296 C486,256 462,236 424,232 C386,230 350,246 340,300 Z" fill="{pelo}" stroke="{LINE}" stroke-width="3"/>')
    b.append(f'<path d="M338,250 C352,206 392,190 430,196 C410,184 372,190 352,214 Z" fill="#2a2420"/>')
    b.append(f'<path d="M350,210 C380,170 440,160 486,196" stroke="#5a6478" stroke-width="3" fill="none" opacity="0.6"/>')
    b.append(f'<path d="M346,236 C376,196 430,186 470,206" stroke="#5a6478" stroke-width="3" fill="none" opacity="0.5"/>')
    b.append('</g>')
    render(sdoc("".join(b), defs), path)
    return path


def todos():
    for e in ("neutral", "triste", "sonrisa"):
        ines(e)
    ines("neutral", chaqueta=False)
    tomas_viejo("neutral"); tomas_viejo("triste")
    lucho("neutral"); lucho("triste")
    arsenio()
    tomas_joven(os.path.join(ARTE, "tomas_joven.png"))
