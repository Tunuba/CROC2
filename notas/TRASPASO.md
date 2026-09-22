# Traspaso, para seguir en otro chat

Estado al 2026-09-22. Proyecto nuevo, empezado hoy. Sigue el mismo patron que
`C:\Proyectos\SABRINA` (mods + descompilacion de un juego PS1) y
`C:\Proyectos\CHAMELEON` (descompilacion N64), pero Croc 2 no arranca de cero:
ya existen herramientas de terceros para los formatos, solo falta el codigo.

## Por que Croc 2 y no otro

Se comparo con Bomberman Hero y con Croc 1 (ver memoria `buscar-decomp-existente-por-la-web-no-solo-por-nombre`):

- **Bomberman Hero (N64)**: ya tiene decomp WIP activo (Bomberhackers/bmhero) y hasta una
  recompilacion jugable (RevoSucks/BMHeroRecomp). Descartado, ya tiene dueno.
- **Croc 1 (PS1)**: decomp de Xeeynamo (github.com/Xeeynamo/croc) parado desde el
  **31 de marzo de 2024**, solo **8.7 %**. Usa **PSY-Q 4.0** como compilador (via decomp.me).
  Se podria retomar, pero no es "sin nada".
- **Croc 2 (PS1)**: **sin decompilacion de codigo**. Solo hay herramientas de extraccion de
  assets (texturas, WAD, sonido) hechas por la comunidad. El ejecutable nunca se toco. Es el
  candidato mas limpio.

## Lo que YA existe (clonado en `herramientas\` para revisar, no se toca el juego)

- **`OverSurge/PS1-Argonaut-Reverse`**: scripts Python (`export_assets.py`,
  `extract_files_from_dat.py`) que extraen WAD/DAT/DIR de los juegos PS1 de Argonaut. Croc 2 y
  su demo estan soportados (✅); Croc 1 no. Documentacion en `Documentation/` (formatos WAD, DEM).
  Discord de la comunidad enlazado en su README.
- **`OverSurge/PS1-Argonaut-Assets`** (no clonado, es el repo con los assets YA extraidos —
  texturas, musica, niveles — de Croc 2, su demo y Harry Potter 1/2. Revisar antes de re-extraer
  nada, puede que ya este ahi).
- **`zeroKilo/Croc2ExplorerWV`**: explorador WAD en C# (.NET, solucion vieja de VS2011), con
  descompresion RLE al vuelo, import/export de texturas PNG y sonidos. Cita como fuente
  `hdc0/Croc-2-mods/doc/wad_files.md`.
- **`hdc0/Croc-2-mods`**: documentacion (`doc/wad_files.md`, `doc/files.md`), un script
  `cvg2wav.py` y un script de Cheat Engine. **OJO: `doc/files.md` es de la version PC de Croc 2**
  (trae `ads.dll`, `Loading.bmp`, archivos sueltos como una instalacion de Windows) — no aplica
  al disco de PS1, comprobado abajo. Sirve solo la documentacion de formatos WAD, no los hashes.

Ninguna de estas cuatro toca el **ejecutable** (`Croc2.exe`/`SLUS_006.34`): todas son de
assets/WAD. La descompilacion del codigo esta completamente sin empezar.

## El disco (ya en mano, 2026-09-22)

Meme bajo `Croc 2 (USA).zip` (Redump, .bin/.cue, pista unica MODE2/2352) y se movio a `disco\`.
Extraido con `dumpsxiso.exe` de las herramientas de Sabrina (reusado, no se instalo de nuevo) a
`extraido\`. `SYSTEM.CNF` dice `BOOT=cdrom:\SLUS_006.34;1`: **el ejecutable real es
`SLUS_006.34`** (163840 bytes en disco, cabecera "PS-X EXE" valida), no "Croc2.exe" de la
documentacion PC. sha256 de `SLUS_006.34`:
`a685d8dd79a37c8b8599ff9adf6ea9e6daebea91ecc5baa1662da5d3b9a112ff`.

Tambien hay un **segundo ejecutable en el disco, `CROC2.EXE`** (403456 bytes, tambien cabecera
PS-X EXE valida) que `SYSTEM.CNF` no arranca directamente — sin investigar aun para que sirve
(¿debug, herramienta interna, build de desarrollo dejada por accidente?). Revisar mas adelante.

Resto del disco: `CROCII.DAT`/`CROCII.DIR` (los assets del juego, formato que ya cubre
PS1-Argonaut-Reverse), pistas de video `.STR` (FOXLOGO, ARGOLOGO, PACK1-6) y audio `.A00` por
nivel.

## Compilador — confirmado, misma familia que Croc 1

Dentro de `SLUS_006.34` hay tres identificadores RCS de Sony sin quitar del build:

```
$Id: intr.c,v 1.75 1997/02/07 09:00:36 makoto Exp $
$Id: sys.c,v 1.140 1998/01/12 07:52:27 noda Exp yos $
$Id: bios.c,v 1.86 1997/03/28 07:42:42 makoto Exp yos $
```

`sys.c`, `bios.c`, `intr.c` son archivos de la libreria de runtime de Sony (LIBPS/LIBSN), y las
fechas (1997-1998) caen justo en la ventana de las PSY-Q 4.x — la misma familia de SDK que uso
Croc 1 (PSY-Q 4.0, confirmado en su README). **Un decomp MATCHING (byte identico) es viable**,
igual que Chameleon Twist con IDO, en vez de la descompilacion funcional que hizo falta en
Sabrina (CodeWarrior, sin compilador disponible). Falta afinar la version exacta de PSY-Q
probando en decomp.me o con los binarios del compilador, cuando se arme el pipeline de verdad.
Script usado: `scripts\buscar_compilador.py` / `buscar_compilador2.py` (buscan strings en el
ejecutable).

## Bloqueos, lo que pone Meme

1. ~~La imagen del disco~~ **Resuelto el 2026-09-22**: Meme puso `Croc 2 (USA).zip` en
   `disco\`, ya extraido.
2. ~~Repo publico o privado~~ **Resuelto el 2026-09-22**: Meme dijo *"privado como sabrina"* —
   misma regla que ahi: **nunca sube nada del juego, ni siquiera el C descompilado ni el asm**
   (`.gitignore` ya actualizado: `decomp/asm/`, `decomp/src/`, `decomp/SLUS_006.34`,
   `decomp/CROC2.EXE`). Solo van al repositorio scripts, notas y (si algun dia hay) parches.
   Distinto de la costumbre de la comunidad de decomp (Xeeynamo/croc, chameleonTwistRet publican
   el C completo) — aqui se sigue el criterio de Meme, no el de la comunidad.
   **Creado y subido el 2026-09-22: github.com/Tunuba/CROC2** (publico, rama main, primer
   commit con notas/scripts/.gitignore nada mas).

## Estructura ya montada (vacia, a la espera del disco)

```
C:\Proyectos\CROC2\
  notas\        <- este archivo
  scripts\      <- vacio, scripts propios (Python) cuando haya algo que sacar
  herramientas\ <- PS1-Argonaut-Reverse, Croc2ExplorerWV, Croc-2-mods (clonados)
  disco\        <- aqui va la imagen que ponga Meme
  extraido\     <- archivos sacados del disco
  decomp\       <- desensamblado y fuente C cuando arranque
  estados\      <- estados guardados del emulador
  .gitignore    <- copiado del patron de SABRINA, ajustar cuando se resuelva el bloqueo 2
```

Sin PCSX-Redux ni Ghidra instalados todavia: se puede reusar lo que ya esta en
`C:\Proyectos\SABRINA\herramientas` (mismo tipo de juego, PS1) en vez de descargar de nuevo,
o instalar aparte con un `arrancar.ps1 -Taller` propio como Sabrina. Decidir cuando haya disco
que analizar.

## Ghidra, primera pasada (2026-09-22)

Reusando Ghidra+JDK de Sabrina (`analyzeHeadless`, proyecto en `ghidra\croc2`), se importo
`SLUS_006.34`. El cargador `ghidra_psx_ldr` ya instalado lo reconocio solo ("PSX Executables
Loader", lenguaje `PSX:LE:32:default:default`) y corrio su analizador de **firmas PSY-Q**
(88 segundos) antes de nada mas. Resultado, exportado a `notas\ghidra\` con
`scripts\ghidra\ExportarTodo.java` (copiado de Sabrina, generico):

- **685 funciones en el rango del juego (0x80100000+)**. De esas, **476 ya vienen con nombre de
  la libreria PSY-Q** (`main`, `start`, `printf`, `sprintf`, `InitGeom`, `SquareRoot12`,
  `ratan2`, `StCdInterrupt`, `_96_init`, `Load`, `Exec`...) — **el 55 % del codigo identificado
  (54196 de 98112 bytes) ya es SDK conocido, no hay que tocarlo.**
- Quedan **209 funciones sin nombre (43916 bytes)**: esas son las candidatas a codigo propio de
  Croc 2, mucho menos que las ~294 KB de Sabrina. `funciones.tsv` tiene la lista completa,
  `decompilado.c` el primer intento de descompilado de Ghidra (referencia, no el C final),
  `textos.tsv` los strings y que funcion los usa.
- Esto **confirma PSY-Q** mas alla de los `$Id` sueltos: las firmas coincidieron con la libreria
  real, no es una coincidencia de fechas.

## Siguiente, en orden

1. Revisar como resolvio `Xeeynamo/croc` el pipeline de matching (de donde saca el compilador
   PSY-Q, Makefile, splat) y reusar ese enfoque en vez de armar uno propio desde cero.
2. Splat sobre `SLUS_006.34` con los simbolos ya sacados (`funciones.tsv`) para partirlo en
   archivos por funcion.
3. Ir cerrando las 209 funciones sin nombre contra el compilador PSY-Q real (decomp.me o
   decomp-permuter) hasta igualar byte a byte.
4. Investigar que es `CROC2.EXE`, el segundo ejecutable del disco (403456 bytes, sin arrancar
   por `SYSTEM.CNF`).
5. Resolver el bloqueo 2 (nombre/visibilidad del repo, y si el C va publico como la comunidad o
   privado como Sabrina) antes de crear el repositorio de GitHub.
