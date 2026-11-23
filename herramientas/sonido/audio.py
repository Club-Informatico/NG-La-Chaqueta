"""Música y efectos originales para LA CHAQUETA (síntesis con numpy)."""
import os
import subprocess
import sys

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 44100
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "game", "audio")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(1968)


def t_(d):
    return np.arange(int(d * SR)) / SR


def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, "low", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi, order=2):
    return sosfilt(butter(order, [lo, hi], "band", fs=SR, output="sos"), x)


def reverb(x, dur=2.8, mezcla=0.35, brillo=5000, seed=0):
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    ir = r.normal(0, 1, n) * np.exp(-np.arange(n) / (SR * dur / 6.5))
    ir = lp(ir, brillo)
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    ir /= np.sqrt(np.sum(ir ** 2))
    if x.ndim == 1:
        w = fftconvolve(x, ir)[: len(x)]
        return x * (1 - mezcla) + w * mezcla * 1.8
    out = np.zeros_like(x)
    for c in range(2):
        irc = np.roll(ir, c * 37)
        out[:, c] = x[:, c] * (1 - mezcla) + fftconvolve(x[:, c], irc)[: len(x)] * mezcla * 1.8
    return out


def estereo(x, ancho=0.0):
    if x.ndim == 2:
        return x
    d = int(0.011 * SR)
    r = np.concatenate([np.zeros(d), x[:-d]])
    return np.stack([x, x * (1 - ancho) + r * ancho], 1)


def normalizar(x, pico=0.89):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * pico


def fundir(x, ini=0.02, fin=0.05):
    n0, n1 = int(ini * SR), int(fin * SR)
    if n0:
        x[:n0] *= np.linspace(0, 1, n0)[:, None] if x.ndim == 2 else np.linspace(0, 1, n0)
    if n1:
        x[-n1:] *= np.linspace(1, 0, n1)[:, None] if x.ndim == 2 else np.linspace(1, 0, n1)
    return x


def plegar(x, L):
    """Bucle sin cortes: todo lo que suena después de L segundos se suma al comienzo."""
    n = int(L * SR)
    y = x[:n].copy()
    resto = x[n:]
    k = min(len(resto), n)
    y[:k] += resto[:k]
    return y


def guardar(nombre, x, q=4):
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = np.stack([x, x], 1)
    pcm = (x * 32767).astype("<i2").tobytes()
    ruta = f"{OUT}/{nombre}.ogg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-",
                    "-c:a", "libvorbis", "-q:a", str(q), ruta], input=pcm, check=True)
    print("ok", ruta, f"{len(x)/SR:.1f}s")


# ---------------------------------------------------------------------------
#  Instrumentos
# ---------------------------------------------------------------------------

def cajita(m, dur=2.5, vel=1.0):
    """Caja de música: tono con parciales inarmónicos y decaimiento rápido."""
    f = mtof(m)
    t = t_(dur)
    tau = 1.4 * (440 / f) ** 0.35
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / tau)
         + 0.28 * np.sin(2 * np.pi * f * 2.0 * t) * np.exp(-t / (tau * 0.5))
         + 0.10 * np.sin(2 * np.pi * f * 3.0 * t) * np.exp(-t / (tau * 0.3))
         + 0.09 * np.sin(2 * np.pi * f * 5.43 * t) * np.exp(-t / 0.06)
         + 0.05 * np.sin(2 * np.pi * f * 8.9 * t) * np.exp(-t / 0.02))
    x *= np.minimum(1, t / 0.002)
    return x * vel


def piano(m, dur=3.0, vel=1.0):
    f = mtof(m)
    t = t_(dur)
    tau = 1.8 * (262 / f) ** 0.4
    x = np.zeros_like(t)
    for k, a in enumerate([1.0, 0.5, 0.28, 0.16, 0.09, 0.05], 1):
        det = 1 + 0.0004 * k * k
        x += a * np.sin(2 * np.pi * f * k * det * t) * np.exp(-t * k ** 0.7 / tau)
    x += 0.04 * rng.normal(0, 1, len(t)) * np.exp(-t / 0.01)
    x *= np.minimum(1, t / 0.004)
    return lp(x, 5200) * vel


def pad(ms, dur, vel=0.3, ataque=2.0, brillo=1400):
    t = t_(dur)
    x = np.zeros_like(t)
    for m in ms:
        f = mtof(m)
        for d in (-0.08, 0.0, 0.07):
            ph = rng.uniform(0, 2 * np.pi)
            # diente de sierra suave (pocas armónicas)
            for k in range(1, 7):
                x += (1 / k) * np.sin(2 * np.pi * f * (1 + d / 100) * k * t + ph * k) / 3
    env = np.minimum(1, t / ataque) * np.minimum(1, (dur - t) / ataque)
    return lp(x * env, brillo) * vel / len(ms)


def guitarra(m, dur=2.0, vel=1.0):
    """Karplus-Strong (con filtro recursivo)."""
    from scipy.signal import lfilter
    f = mtof(m)
    n = int(SR / f)
    N = int(dur * SR)
    exc = np.zeros(N)
    exc[:n] = rng.uniform(-1, 1, n)
    a = np.zeros(n + 2)
    a[0] = 1.0
    a[n] = -0.4985
    a[n + 1] = -0.4985
    out = lfilter([1.0], a, exc)
    return lp(out, 3500) * vel


def golpe(f0=60, dur=0.35, ruido=0.2, f1=None):
    t = t_(dur)
    f1 = f1 or f0 * 0.6
    fr = f1 + (f0 - f1) * np.exp(-t / 0.04)
    ph = 2 * np.pi * np.cumsum(fr) / SR
    x = np.sin(ph) * np.exp(-t / (dur / 4))
    x += ruido * lp(rng.normal(0, 1, len(t)), 2000) * np.exp(-t / 0.02)
    return x


def mezclar(dst, src, inicio):
    i = int(inicio * SR)
    if i < 0:
        src = src[-i:]
        i = 0
    j = min(len(dst), i + len(src))
    if j > i:
        dst[i:j] += src[: j - i]


# ---------------------------------------------------------------------------
#  Música
# ---------------------------------------------------------------------------

# Melodía original de Inés (vals lento en La menor). (nota MIDI, pulsos)
MELODIA = [(76, 2), (74, 1), (72, 1), (71, 1), (69, 1), (71, 2), (64, 1), (69, 3),
           (72, 2), (74, 1), (76, 1), (77, 1), (76, 1), (74, 2), (71, 1), (76, 3),
           (76, 2), (74, 1), (72, 1), (71, 1), (69, 1), (77, 2), (76, 1), (74, 1), (72, 1), (71, 1),
           (72, 2), (71, 1), (69, 1), (68, 1), (71, 1), (69, 3), (None, 3)]
ACORDES = [(45, [57, 60, 64]), (45, [57, 60, 64]), (40, [56, 59, 64]), (45, [57, 60, 64]),
           (41, [57, 60, 65]), (48, [55, 60, 64]), (38, [57, 62, 65]), (40, [56, 59, 62]),
           (45, [57, 60, 64]), (45, [57, 60, 64]), (38, [57, 62, 65]), (43, [55, 59, 62]),
           (41, [57, 60, 65]), (40, [56, 59, 64]), (45, [57, 60, 64]), (45, [57, 60, 64])]


def tema_ines():
    pulso = 60 / 80
    compases = 16
    L = compases * 3 * pulso * 2
    total = L + 4
    x = np.zeros(int(total * SR))
    for vuelta in range(2):
        t0 = vuelta * compases * 3 * pulso
        t = t0
        for (m, d) in MELODIA:
            if m is not None:
                mm = m + (12 if vuelta == 1 else 0)
                mezclar(x, cajita(mm, 2.8, 0.55 + 0.1 * rng.random()), t + rng.uniform(-0.01, 0.01))
                if vuelta == 1:
                    mezclar(x, cajita(m, 2.8, 0.25), t + 0.01)
            t += d * pulso
        for c, (bajo, ac) in enumerate(ACORDES):
            tb = t0 + c * 3 * pulso
            mezclar(x, cajita(bajo + 12, 2.5, 0.35), tb)
            for k, nota in enumerate(ac[1:]):
                mezclar(x, cajita(nota, 1.6, 0.16), tb + pulso * (1 + k))
    x = hp(x, 120)
    x = estereo(x, 0.5)
    x = reverb(x, 3.2, 0.42, 6000, seed=3)
    x = plegar(x, L)
    guardar("tema_ines", normalizar(x, 0.6))


def noche_copiapo():
    dur = 64.0
    x = np.zeros(int((dur + 7) * SR))
    prog = [[45, 57, 60, 64], [41, 57, 60, 65], [48, 55, 60, 64], [43, 55, 59, 62]]
    seg = dur / 8
    for i in range(8):
        ac = prog[i % 4]
        mezclar(x, pad(ac, seg + 2.5, 0.5, ataque=2.2, brillo=900), i * seg)
        mezclar(x, piano(ac[0] + 12, 4, 0.18), i * seg + 0.2)
    # notas sueltas de piano, como gotas
    notas = [76, 72, 74, 71, 69, 76, 79, 77, 76, 74, 72, 71]
    for k in range(14):
        tt = 3 + k * 4.3 + rng.uniform(-0.6, 0.6)
        if tt < dur - 4:
            mezclar(x, piano(notas[k % len(notas)], 4, 0.16), tt)
    # pulso grave lento
    for k in range(int(dur / 2.0)):
        mezclar(x, golpe(48, 0.9, 0.0) * 0.18, k * 2.0)
    x = hp(x, 40)
    x = estereo(x, 0.6)
    x = reverb(x, 3.5, 0.45, 3500, seed=4)
    x = plegar(x, dur)
    guardar("noche_copiapo", normalizar(x, 0.6))


def tension():
    dur = 48.0
    t = t_(dur + 5)
    x = 0.4 * np.sin(2 * np.pi * mtof(33) * t) + 0.32 * np.sin(2 * np.pi * mtof(34) * t + 1)
    x += 0.15 * np.sin(2 * np.pi * mtof(45) * t) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 12))
    ruido = bp(rng.normal(0, 1, len(t)), 200, 900)
    x += 0.25 * ruido * (0.5 + 0.5 * np.sin(2 * np.pi * t / 8 - 1.5)) ** 3
    x[int(dur * SR):] *= np.linspace(1, 0, len(x) - int(dur * SR))
    # latido lejano
    for k in range(int(dur / 1.6)):
        mezclar(x, golpe(55, 0.4, 0.05) * 0.5, k * 1.6)
        mezclar(x, golpe(50, 0.35, 0.03) * 0.35, k * 1.6 + 0.28)
    # campanitas metálicas disonantes
    for k in range(9):
        tt = 2 + k * 5.1 + rng.uniform(-1, 1)
        m = int(rng.choice([82, 83, 87, 89, 94]))
        mezclar(x, cajita(m, 4, 0.12), tt)
    x = estereo(x, 0.7)
    x = reverb(x, 4.0, 0.5, 2500, seed=5)
    x = plegar(x, dur)
    guardar("tension", normalizar(x, 0.6))


def amanecer():
    pulso = 60 / 66
    mel = [(m + (1 if m in (72, 77, 79, 60, 65, 67) else 0) if m else None, d) for m, d in MELODIA]  # La mayor
    acordes = [(45, [57, 61, 64]), (45, [57, 61, 64]), (40, [56, 59, 64]), (45, [57, 61, 64]),
               (42, [57, 61, 66]), (49, [56, 61, 64]), (38, [57, 62, 66]), (40, [56, 59, 62]),
               (45, [57, 61, 64]), (45, [57, 61, 64]), (38, [57, 62, 66]), (44, [56, 59, 64]),
               (42, [57, 61, 66]), (40, [56, 59, 64]), (45, [57, 61, 64]), (45, [57, 61, 64])]
    L = 16 * 3 * pulso
    x = np.zeros(int((L + 6) * SR))
    t = 0.0
    for (m, d) in mel:
        if m is not None:
            mezclar(x, piano(m, 3.5, 0.5), t)
        t += d * pulso
    for c, (bajo, ac) in enumerate(acordes):
        tb = c * 3 * pulso
        mezclar(x, piano(bajo, 4, 0.35), tb)
        mezclar(x, pad(ac, 3 * pulso + 1.5, 0.35, ataque=0.8, brillo=1600), tb)
        for k, nota in enumerate(ac):
            mezclar(x, piano(nota, 2.5, 0.12), tb + pulso * (1 + (k % 2)))
    x = hp(x, 50)
    x = estereo(x, 0.5)
    x = reverb(x, 3.0, 0.38, 6000, seed=6)
    x = plegar(x, L)
    guardar("amanecer", normalizar(x, 0.65))


def radio_bolero():
    """Un bolero original que suena 'por radio de tubo' (filtrado + crepitar)."""
    pulso = 60 / 92
    mel = [(69, 1.5), (72, 0.5), (76, 2), (74, 1), (72, 1), (71, 2), (None, 2),
           (68, 1.5), (71, 0.5), (74, 2), (72, 1), (71, 1), (69, 3), (None, 1),
           (69, 1.5), (72, 0.5), (77, 2), (76, 1), (74, 1), (72, 1.5), (71, 0.5), (69, 2),
           (71, 1), (72, 1), (71, 1), (68, 1), (69, 4)]
    acordes = [(45, [57, 60, 64]), (45, [57, 60, 64]), (40, [56, 59, 62]), (40, [56, 59, 64]),
               (40, [56, 59, 62]), (45, [57, 60, 64]), (41, [57, 60, 65]), (45, [57, 60, 64]),
               (40, [56, 59, 62]), (45, [57, 60, 64])]
    total = 10 * 4 * pulso + 3
    x = np.zeros(int(total * SR))
    t = 0.2
    for (m, d) in mel:
        if m is not None:
            mezclar(x, guitarra(m, d * pulso + 0.8, 0.7), t)
            mezclar(x, guitarra(m - 12, d * pulso + 0.5, 0.25), t + 0.01)
        t += d * pulso
    for c, (bajo, ac) in enumerate(acordes):
        tb = 0.2 + c * 4 * pulso
        mezclar(x, guitarra(bajo, 1.2, 0.6), tb)
        mezclar(x, guitarra(bajo + 7, 1.0, 0.4), tb + 2 * pulso)
        for k in (1, 1.5, 3, 3.5):
            for j, nota in enumerate(ac):
                mezclar(x, guitarra(nota, 0.5, 0.18), tb + k * pulso + j * 0.012)
        # ritmo de bolero: maracas y bongó
        for k in (0, 1, 1.5, 2, 3, 3.5):
            mezclar(x, hp(rng.normal(0, 1, int(0.05 * SR)), 5000) * np.exp(-t_(0.05) / 0.012) * 0.15, tb + k * pulso)
        for k, f in ((1.5, 380), (3, 300), (3.5, 380)):
            mezclar(x, golpe(f, 0.18, 0.1, f1=f * 0.9) * 0.18, tb + k * pulso)
    # radio: banda estrecha, saturación suave, ondulación y crepitar
    x = bp(x, 350, 2800, 3)
    x = np.tanh(x * 2.5) * 0.6
    tt = t_(len(x) / SR)
    x *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * tt)
    crep = np.zeros_like(x)
    idx = rng.integers(0, len(x), 350)
    crep[idx] = rng.uniform(-0.25, 0.25, len(idx))
    x += lp(crep, 4000) + 0.008 * bp(rng.normal(0, 1, len(x)), 1000, 5000)
    x = fundir(x, 0.6, 2.0)
    guardar("radio_bolero", normalizar(x, 0.7))


# ---------------------------------------------------------------------------
#  Efectos
# ---------------------------------------------------------------------------

def viento_noche():
    dur = 40.0
    t = t_(dur)
    n = rng.normal(0, 1, len(t))
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * t / 10.0) * np.sin(2 * np.pi * t / 20.0 + 1)
    viento = lp(n, 500) * (0.25 + 0.75 * lfo) + 0.3 * bp(n, 600, 1400) * lfo ** 2
    x = viento * 0.6
    # grillos
    for k in range(int(dur * 1.3)):
        tt = rng.uniform(0, dur - 1)
        f = rng.uniform(4300, 4800)
        n_ch = int(rng.integers(2, 5))
        for j in range(n_ch):
            d = 0.035
            s = np.sin(2 * np.pi * f * t_(d)) * np.sin(np.pi * t_(d) / d) * 0.035
            mezclar(x, s, tt + j * 0.06)
    x = estereo(x, 0.8)
    x = np.concatenate([x, np.zeros((int(2 * SR), 2))])
    x = reverb(x, 1.5, 0.2, 4000, seed=9)
    x = plegar(x, dur)
    guardar("viento_noche", normalizar(x, 0.5))


def motor():
    dur = 8.0
    t = t_(dur)
    f = 31 + 0.6 * np.sin(2 * np.pi * 0.625 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.35 * np.sin(3 * ph + 0.3) + 0.2 * np.sin(4 * ph)
    x = np.sign(x) * np.abs(x) ** 0.8
    ruido = rng.normal(0, 1, len(t))
    x = lp(x, 220) + 0.08 * lp(ruido, 300)
    guardar("motor", normalizar(x, 0.22))


def puerta():
    x = np.zeros(int(1.2 * SR))
    mezclar(x, golpe(75, 0.5, 0.6, f1=50), 0.0)
    mezclar(x, hp(rng.normal(0, 1, int(0.03 * SR)), 2500) * 0.3 * np.exp(-t_(0.03) / 0.006), 0.0)
    mezclar(x, golpe(160, 0.15, 0.3) * 0.3, 0.02)
    x = reverb(x, 0.6, 0.15, 3000, seed=10)
    guardar("puerta", normalizar(fundir(x, 0, 0.2), 0.8))


def toc():
    x = np.zeros(int(1.6 * SR))
    for k in range(3):
        s = np.sin(2 * np.pi * 1150 * t_(0.12)) * np.exp(-t_(0.12) / 0.015)
        s += 0.6 * np.sin(2 * np.pi * 2900 * t_(0.12)) * np.exp(-t_(0.12) / 0.008)
        s += 0.3 * hp(rng.normal(0, 1, len(s)), 3000) * np.exp(-t_(0.12) / 0.004)
        mezclar(x, s * (0.8 + 0.1 * k), 0.05 + k * 0.38)
    x = reverb(x, 0.8, 0.2, 6000, seed=11)
    guardar("toc", normalizar(fundir(x, 0, 0.2), 0.7))


def tic():
    x = np.zeros(int(0.6 * SR))
    s = np.sin(2 * np.pi * 2100 * t_(0.06)) * np.exp(-t_(0.06) / 0.01)
    mezclar(x, s, 0.01)
    mezclar(x, golpe(900, 0.05, 0.4) * 0.3, 0.0)
    x = reverb(x, 1.8, 0.35, 5000, seed=12)
    guardar("tic", normalizar(fundir(x, 0, 0.1), 0.55))


def estatica():
    dur = 6.0
    t = t_(dur)
    x = bp(rng.normal(0, 1, len(t)), 500, 5000) * 0.35
    crep = np.zeros_like(t)
    idx = rng.integers(0, len(t), 1500)
    crep[idx] = rng.uniform(-1, 1, len(idx))
    x += lp(crep, 6000) * 0.5
    # silbido de sintonía
    f = 900 + 700 * np.sin(2 * np.pi * t / 3.5)
    x += 0.12 * np.sin(2 * np.pi * np.cumsum(f) / SR) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 1.7))
    x *= 0.7 + 0.3 * np.sin(2 * np.pi * 3.3 * t)
    guardar("estatica", normalizar(fundir(x, 0.05, 0.4), 0.5))


def latido():
    x = np.zeros(int(3.6 * SR))
    for k in range(3):
        mezclar(x, golpe(58, 0.35, 0.05, f1=40), 0.05 + k * 1.05)
        mezclar(x, golpe(50, 0.3, 0.03, f1=36) * 0.7, 0.05 + k * 1.05 + 0.27)
    x = lp(x, 400)
    x = reverb(x, 1.2, 0.2, 800, seed=13)
    guardar("latido", normalizar(fundir(x, 0, 0.3), 0.9))


def reja():
    dur = 2.8
    t = t_(dur)
    f = 420 + 260 * np.sin(np.pi * t / dur * 1.3) + 40 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    chirrido = (np.sin(ph) + 0.5 * np.sin(2.01 * ph) + 0.3 * np.sin(3.03 * ph))
    am = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 23 * t))) * 0.6 + 0.4
    x = chirrido * am * np.sin(np.pi * np.minimum(t / dur, 1)) ** 0.5 * 0.4
    x = bp(x, 300, 4000)
    # cadena cayendo
    for k in range(9):
        s = np.sin(2 * np.pi * rng.uniform(2500, 4200) * t_(0.15)) * np.exp(-t_(0.15) / 0.03)
        s += 0.4 * np.sin(2 * np.pi * rng.uniform(5000, 7000) * t_(0.15)) * np.exp(-t_(0.15) / 0.015)
        mezclar(x, s * 0.25, 0.02 + k * 0.07 + rng.uniform(0, 0.03))
    x = reverb(x, 1.6, 0.3, 5000, seed=14)
    guardar("reja", normalizar(fundir(x, 0, 0.3), 0.7))


TODO = ["tema_ines", "noche_copiapo", "tension", "amanecer", "radio_bolero",
        "viento_noche", "motor", "puerta", "toc", "tic", "estatica", "latido", "reja"]

if __name__ == "__main__":
    for n in sys.argv[1:] or TODO:
        globals()[n]()
