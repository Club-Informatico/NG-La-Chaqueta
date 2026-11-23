"""Validador estático (aproximado) para el proyecto Ren'Py de LA CHAQUETA.

No reemplaza a 'Lint' de Ren'Py, pero revisa lo que suele romper un guion:
indentación, labels, saltos, imágenes, audio, transformaciones, personajes,
etiquetas de texto y bloques de Python.
"""
import ast
import os
import re
import sys

# Por defecto revisa la carpeta "game" del repositorio (../game respecto a este archivo).
# También puedes pasar otra ruta: python herramientas/validar_renpy.py C:/ruta/a/tu/proyecto/game
GAME = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "game")
if not os.path.isdir(GAME):
    sys.exit(f"No existe la carpeta del juego: {GAME}")
errores, avisos = [], []

files = [f for f in os.listdir(GAME) if f.endswith(".rpy")]
src = {f: open(os.path.join(GAME, f), encoding="utf-8").read() for f in files}

labels, images, audio, transforms, chars, defaults, transitions = set(), {}, {}, set(), set(), set(), set()
BUILTIN_TRANS = {"dissolve", "fade", "hpunch", "vpunch", "move", "pixellate", "None", "ease", "moveinleft", "moveinright"}
BUILTIN_POS = {"left", "right", "center", "truecenter", "topleft", "topright"}
BUILTIN_CHARS = {"centered", "narrator", "nvl", "extend"}

for f, s in src.items():
    for i, line in enumerate(s.split("\n"), 1):
        if "\t" in line:
            errores.append(f"{f}:{i}: tabulación (usar espacios)")
        st = line.strip()
        ind = len(line) - len(line.lstrip(" "))
        if st and ind % 4:
            errores.append(f"{f}:{i}: indentación no múltiplo de 4")
        m = re.match(r"label (\w+)\s*:", st)
        if m:
            if m.group(1) in labels:
                errores.append(f"{f}:{i}: label duplicado {m.group(1)}")
            labels.add(m.group(1))
        m = re.match(r'image ([\w ]+?)\s*=\s*(.+)$', st)
        if m:
            name = " ".join(m.group(1).split())
            images[name] = m.group(2)
        m = re.match(r'define audio\.(\w+)\s*=\s*"(.+)"', st)
        if m:
            audio[m.group(1)] = m.group(2)
        m = re.match(r"transform (\w+)", st)
        if m:
            transforms.add(m.group(1))
        m = re.match(r"define (\w+)\s*=\s*Character\(", st)
        if m:
            chars.add(m.group(1))
        m = re.match(r"define (\w+)\s*=\s*(Fade|Dissolve|MoveTransition)\(", st)
        if m:
            transitions.add(m.group(1))
        m = re.match(r"default (\w+)\s*=", st)
        if m:
            defaults.add(m.group(1))

# archivos de imagen y audio existen
for n, v in images.items():
    m = re.match(r'"(.+)"', v)
    if m and not os.path.exists(os.path.join(GAME, m.group(1))):
        errores.append(f"imagen '{n}': falta el archivo {m.group(1)}")
for n, p in audio.items():
    if not os.path.exists(os.path.join(GAME, p)):
        errores.append(f"audio '{n}': falta el archivo {p}")

tags = {k.split()[0] for k in images}
s = src["script.rpy"]
lines = s.split("\n")
pila_menu = []
for i, line in enumerate(lines, 1):
    st = line.strip()
    if not st or st.startswith("#"):
        continue
    # saltos
    for kw in ("jump", "call"):
        m = re.match(rf"{kw} (\w+)", st)
        if m and m.group(1) not in labels:
            errores.append(f"script.rpy:{i}: {kw} a label inexistente '{m.group(1)}'")
    # scene/show/hide
    m = re.match(r"(scene|show|hide) ([\w ]+?)(?:\s+(?:at|with|as|behind|zorder)\b.*)?$", st)
    if m:
        cmd, name = m.group(1), " ".join(m.group(2).split())
        if cmd == "hide":
            if name.split()[0] not in tags:
                errores.append(f"script.rpy:{i}: hide de tag desconocido '{name}'")
        elif name not in images:
            errores.append(f"script.rpy:{i}: imagen no definida '{name}'")
        at = re.search(r"\bat ([\w(). ,]+?)(?:\s+with\b|$)", st)
        if at:
            for tr in at.group(1).split(","):
                trn = tr.strip().split("(")[0]
                if trn not in transforms and trn not in BUILTIN_POS:
                    errores.append(f"script.rpy:{i}: transform desconocida '{trn}'")
    # transiciones
    for w in re.findall(r"\bwith (\w+)", st):
        if w not in transitions and w not in BUILTIN_TRANS:
            errores.append(f"script.rpy:{i}: transición desconocida '{w}'")
    # audio
    m = re.match(r"play (\w+) (\w+|\"[^\"]+\")(.*)$", st)
    if m:
        ch, snd, rest = m.groups()
        if ch not in ("music", "sound", "voice", "ambiente", "motor"):
            errores.append(f"script.rpy:{i}: canal desconocido {ch}")
        if not snd.startswith('"') and snd not in audio:
            errores.append(f"script.rpy:{i}: audio no definido '{snd}'")
        rest_ok = re.fullmatch(r"(\s+(fadein|fadeout) [0-9.]+|\s+noloop|\s+loop|\s+if_changed)*\s*", rest)
        if not rest_ok:
            errores.append(f"script.rpy:{i}: cláusulas raras en play: '{rest}'")
    m = re.match(r"stop (\w+)", st)
    if m and m.group(1) not in ("music", "sound", "voice", "ambiente", "motor"):
        errores.append(f"script.rpy:{i}: stop de canal desconocido")
    # diálogo con personaje
    m = re.match(r'(\w+) "(.*)"(\s+with \w+)?$', st)
    if m and m.group(1) not in ("jump", "call", "play", "show", "scene", "hide"):
        who = m.group(1)
        if who not in chars and who not in BUILTIN_CHARS:
            errores.append(f"script.rpy:{i}: personaje no definido '{who}'")
    # texto: comillas y etiquetas
    for txt in re.findall(r'"((?:[^"\\]|\\.)*)"', st):
        if "[" in txt:
            for var in re.findall(r"\[(\w+)\]", txt):
                if var not in defaults:
                    errores.append(f"script.rpy:{i}: interpolación de variable desconocida [{var}]")
            if re.search(r"\[(?!\w+\])", txt):
                errores.append(f"script.rpy:{i}: '[' suelto en texto")
        abiertas = []
        for tg in re.findall(r"\{(/?)(\w+)(?:=[^}]*)?\}", txt):
            cierre, nombre = tg
            if nombre in ("w", "p", "nw", "fast", "done"):
                continue
            if cierre:
                if not abiertas or abiertas[-1] != nombre:
                    errores.append(f"script.rpy:{i}: etiqueta de texto mal cerrada {{/{nombre}}}")
                else:
                    abiertas.pop()
            else:
                abiertas.append(nombre)
        if abiertas:
            errores.append(f"script.rpy:{i}: etiqueta de texto sin cerrar {abiertas}")
        if "%" in txt:
            avisos.append(f"script.rpy:{i}: '%' en texto")
    if st.count('"') % 2:
        errores.append(f"script.rpy:{i}: comillas desbalanceadas")
    # python en línea
    if st.startswith("$ "):
        try:
            ast.parse(st[2:])
        except SyntaxError as e:
            errores.append(f"script.rpy:{i}: Python inválido: {e}")
    m = re.match(r"(if|elif) (.+):$", st)
    if m:
        try:
            ast.parse(m.group(2), mode="eval")
        except SyntaxError as e:
            errores.append(f"script.rpy:{i}: condición inválida: {e}")
        sin_textos = re.sub(r'"(?:[^"\\]|\\.)*"', '""', m.group(2))  # ignora palabras entre comillas
        for var in re.findall(r"\b([a-z_]+)\b", sin_textos):
            if var not in defaults and var not in ("in", "not", "and", "or", "len", "True", "False", "None"):
                avisos.append(f"script.rpy:{i}: variable '{var}' en condición no tiene default")

# estructura de bloques: una línea que termina en ':' debe ir seguida de algo más indentado
for i in range(len(lines) - 1):
    st = lines[i].rstrip()
    if st.strip().endswith(":") and not st.strip().startswith("#"):
        ind = len(st) - len(st.lstrip())
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j < len(lines):
            ind2 = len(lines[j]) - len(lines[j].lstrip())
            if ind2 <= ind:
                errores.append(f"script.rpy:{i+1}: bloque vacío después de ':'")

# cada label debería terminar en jump/return (sin caer a otro label)
cur = None
ult = None
for i, line in enumerate(lines, 1):
    st = line.strip()
    if re.match(r"label \w+:", st):
        if cur and ult and not re.match(r"(jump|return)\b", ult):
            avisos.append(f"label '{cur}' termina con '{ult[:40]}' (cae al siguiente label)")
        cur = st[6:-1]
    elif st and not st.startswith("#") and line.startswith("    ") and not line.startswith("        "):
        ult = st
if cur and ult and not re.match(r"(jump|return)\b", ult):
    avisos.append(f"label '{cur}' no termina en jump/return")

# imágenes/audio no usados (informativo)
usadas = set(re.findall(r"(?:scene|show) ([\w]+ [\w]+|negro)", s))
for n in images:
    if n not in usadas:
        avisos.append(f"imagen definida y no usada: {n}")
for n in audio:
    if not re.search(rf"\b{n}\b", s):
        avisos.append(f"audio definido y no usado: {n}")

print(f"labels: {len(labels)} · imágenes: {len(images)} · audios: {len(audio)} · personajes: {sorted(chars)}")
print(f"ERRORES ({len(errores)}):")
for e in errores:
    print("  ", e)
print(f"AVISOS ({len(avisos)}):")
for a in avisos:
    print("  ", a)
sys.exit(1 if errores else 0)
