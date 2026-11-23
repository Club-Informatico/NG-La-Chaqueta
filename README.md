# La Chaqueta · Una leyenda de Copiapó

Novela visual de terror y misterio, ambientada en Copiapó (Chile) y hecha con [Ren'Py](https://www.renpy.org).

![Ren'Py 8.x](https://img.shields.io/badge/Ren'Py-8.x-ff7f50)
![Resolución 1920x1080](https://img.shields.io/badge/resoluci%C3%B3n-1920x1080-blue)
![Idioma: español](https://img.shields.io/badge/idioma-espa%C3%B1ol-yellow)
![Licencia GPL-3.0](https://img.shields.io/badge/licencia-GPL--3.0-green)

> Copiapó, domingo 8 de noviembre. Rodolfo Pizarro, taxista nocturno, recoge bajo los pimientos de la Plaza Prat a una muchacha que lleva una chaqueta de lana roja que le queda enorme. Le da una dirección que parece de lo más normal: *"Pasaje Los Pimientos 2347"*. El reloj del auto se detiene a las 23:47, el taxímetro marca en escudos… y la chaqueta se queda en el asiento.

- **Duración:** entre 20 y 30 minutos de lectura
- **Estructura:** prólogo, 6 capítulos y epílogo
- **Arte y sonido:** originales, generados por código (los scripts están en [`herramientas/`](herramientas/))

<!-- Sugerencia: agrega aquí una captura, por ejemplo:
![Portada](docs/portada.png)
-->

---

## Contenido

- [Cómo jugarla](#cómo-jugarla)
- [Solución de problemas](#solución-de-problemas)
- [Personajes](#personajes)
- [Decisiones del jugador](#decisiones-del-jugador)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Cómo personalizarla](#cómo-personalizarla)
- [Regenerar el arte o el sonido](#regenerar-el-arte-o-el-sonido)
- [Sobre la ambientación](#sobre-la-ambientación)
- [Licencia](#licencia)

---

## Cómo jugarla

Este repositorio trae **solo los archivos del juego**: guion, imágenes, audio y fuentes. Los archivos base de la interfaz (`gui.rpy`, `screens.rpy` y `options.rpy`) los crea el launcher de Ren'Py, así que primero hay que crear un proyecto vacío.

1. Descarga **Ren'Py 8** desde [renpy.org](https://www.renpy.org) y abre el *Ren'Py Launcher*.
2. Haz clic en **"+ Crear nuevo proyecto"** y configúralo así:
   - **Nombre:** `La Chaqueta`
   - **Resolución:** `1920x1080` ⚠️ *Es importante: con otra resolución las imágenes quedan descentradas o recortadas.*
   - **Esquema de color:** el que quieras (se ve mejor uno oscuro).
3. Descarga este repositorio con `git clone` o con **Code → Download ZIP**:
   ```bash
   git clone https://github.com/Club-Informatico/NG-La-Chaqueta.git
   ```
4. En el launcher, con tu proyecto seleccionado, haz clic en **"Abrir directorio → game"**.
5. Copia **todo el contenido** de la carpeta [`game/`](game/) del repositorio dentro de esa carpeta `game` y acepta reemplazar los archivos que ya existen (`script.rpy`).
6. En el launcher, haz clic en **"Revisar script (Lint)"** y después en **"Lanzar proyecto"**.

### En macOS

Al copiar una carpeta encima de otra con el mismo nombre, el Finder **reemplaza la carpeta completa** en vez de combinarlas. Eso borra los archivos que creó Ren'Py. Para evitarlo, usa una de estas dos opciones:

- **Finder:** mantén presionada la tecla **Opción (⌥)** mientras arrastras y elige **"Combinar"** (no "Reemplazar").
- **Terminal:** cambia las rutas por las tuyas.
  ```bash
  ditto ~/Downloads/NG-La-Chaqueta/game ~/RUTA/A/TU/PROYECTO/game
  ```

Si ya reemplazaste la carpeta `game` completa, lo más simple es crear un proyecto nuevo en el launcher y volver a copiar.

---

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| Las imágenes salen descentradas, recortadas o más grandes que la ventana | El proyecto no está en 1920x1080, o no tiene `gui.rpy` | Revisa que `game/gui.rpy` diga `gui.init(1920, 1080)`. Si falta, crea el proyecto desde el launcher (ver arriba). |
| Error `'Layout' object has no attribute 'yesno_prompt'` al salir | Falta `screens.rpy` porque no se creó el proyecto desde el launcher | Crea un proyecto nuevo en el launcher y copia ahí la carpeta `game`. |
| Aviso del Lint: *"gui.main_menu_background ya está definida en gui.rpy"* | Es esperado: el juego cambia el fondo del menú | Puedes ignorarlo. |
| El guion se rompe después de editarlo | El editor cambió las comillas por comillas tipográficas (“ ”) | Edita los `.rpy` con un editor de código, como Visual Studio Code. |

Ren'Py guarda `log.txt` y, si hubo un error, `traceback.txt` en la carpeta del proyecto, junto a `game/`. Ahí aparece la causa del problema. Después de cambiar archivos, cierra el juego antes de volver a lanzarlo.

---

## Personajes

| Personaje | En el guion | Descripción |
|---|---|---|
| **Rodolfo Pizarro** | *(narrador)* | Taxista nocturno de Copiapó |
| **La pasajera** | `p` | La muchacha de la chaqueta roja |
| **Tomás** | `t` | El papá de Rodolfo |
| **Don Lucho** | `l` | El taxista más antiguo de Copiapó |
| **Don Arsenio** | `a` | Cuidador del cementerio |

---

## Decisiones del jugador

- Dar vuelta (o no) la foto que está boca abajo en la casa de tu papá. Si la ves, después reconoces la palomita de plata.
- En el taxi eliges **2 de 3 acciones**: preguntarle de dónde viene, prender la radio o mirarla por el espejo. Cada una da pistas distintas.
- Bajarte a buscarla o quedarte en el taxi.
- Mostrarle la chaqueta a Don Lucho o solo preguntarle por la dirección.
- Abrir el sobre o no abrirlo.
- Cómo contarle todo a tu papá.
- Encarar a Don Lucho o esperar.
- Lo que le dices a la pasajera al final. Esto cambia su respuesta y la reflexión final del epílogo.

Todas las rutas llegan al **mismo final cerrado**. Las decisiones cambian diálogos, pistas y detalles.

---

## Estructura del repositorio

```
game/
├── script.rpy                 Guion completo (prólogo, 6 capítulos y epílogo)
├── leyenda_definiciones.rpy   Personajes, imágenes, transiciones, canales de sonido y estilo de texto
├── images/
│   ├── bg/                    11 fondos (.webp, 1920x1080)
│   ├── cg/                    12 escenas especiales y la portada (.webp, 1920x1080)
│   ├── sprites/               9 sprites de personajes (.png con transparencia, 820x1080)
│   └── menu/                  Fondos del menú principal y de los menús internos
├── audio/                     5 piezas de música y 8 efectos (.ogg), originales
└── fonts/                     DejaVu Serif (licencia libre incluida)

herramientas/
├── arte/                      Scripts que generan fondos, sprites y escenas especiales
├── sonido/                    Script que sintetiza la música y los efectos
└── validar_renpy.py           Revisión rápida del guion
```

---

## Cómo personalizarla

- **Textos:** todo el guion está en [`game/script.rpy`](game/script.rpy). Las líneas entre comillas sin nombre delante son la voz de Rodolfo.
- **Imágenes:** puedes reemplazar cualquier archivo por otro con el **mismo nombre**. Si cambias la extensión (por ejemplo, de `.webp` a `.png`), actualiza la línea correspondiente en [`game/leyenda_definiciones.rpy`](game/leyenda_definiciones.rpy).
  - Fondos y escenas especiales: **1920x1080**
  - Sprites: **820x1080**, PNG con fondo transparente
- **Música:** los temas están definidos en `leyenda_definiciones.rpy` como `audio.tema_ines`, `audio.noche`, `audio.tension`, `audio.amanecer` y `audio.bolero`.

---

## Regenerar el arte o el sonido

Es opcional: el repositorio ya trae todos los recursos generados.

**Requisitos:** Python 3 con `numpy`, `scipy` y `Pillow`, además de [`rsvg-convert`](https://wiki.gnome.org/Projects/LibRsvg) (librsvg) y [`ffmpeg`](https://ffmpeg.org) en el `PATH`.

```bash
pip install numpy scipy pillow

cd herramientas/arte
python fondos.py
python sprites.py
python cgs.py

cd ../sonido
python audio.py
```

Los scripts escriben directamente en la carpeta `game/` del repositorio y usan rutas relativas, así que funcionan igual en Windows, macOS y Linux. Las imágenes intermedias quedan en `herramientas/arte/_trabajo/`.

> **Nota:** `fondos.py` y `cgs.py` generan archivos `.png`, pero el proyecto usa `.webp` para que pese menos. Puedes convertirlos o cambiar las extensiones en `leyenda_definiciones.rpy`.

### Validar el guion

```bash
python herramientas/validar_renpy.py                       # revisa game/ de este repositorio
python herramientas/validar_renpy.py ruta/a/tu/proyecto/game
```

Revisa indentación, labels, saltos, imágenes, audio, transformaciones, personajes y etiquetas de texto. **No reemplaza el Lint de Ren'Py.**

---

## Sobre la ambientación

La Plaza Prat con sus pimientos, la avenida Copayapu, el cementerio de la avenida La Paz y la salida a Tierra Amarilla son lugares reales de Copiapó.

Los personajes, la Radio Chañarcillo, la empresa "Estrella del Norte" y el "Pasaje Los Pimientos" dentro del cementerio son inventados para la historia.

Los escudos (E°) fueron la moneda de Chile entre 1960 y 1975.

---

## Licencia

El juego se distribuye bajo la licencia **GNU GPL v3.0**. Consulta el archivo [LICENSE](LICENSE).

La fuente **DejaVu Serif** tiene su propia licencia libre, incluida en [`game/fonts/LICENCIA-DejaVu.txt`](game/fonts/LICENCIA-DejaVu.txt).
