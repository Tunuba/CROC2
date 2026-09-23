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

## CORRECCION IMPORTANTE: el juego de verdad es CROC2.EXE, no SLUS_006.34 (2026-09-22)

Todo el pipeline de abajo se armo apuntando a `SLUS_006.34` pensando que era el ejecutable
principal. **Es al reves: `SLUS_006.34` es solo un cargador chico.** Dentro de el hay el string
literal `cdrom:\CROC2.EXE;1` (visto con `scripts\buscar_croc2exe_ref.py`) y trae las funciones
PSY-Q `Load`/`Exec` — es el patron clasico de un stage0 que carga el ejecutable real desde el
disco y le salta.

Se importo `extraido\CROC2.EXE` en el mismo proyecto Ghidra (`ghidra\croc2`), mismo metodo que
`SLUS_006.34` (PsyQ Signatures corrio 122 segundos), exportado a `notas\ghidra\croc2exe\`:

- **972 funciones reales** (contra 685 de SLUS_006.34). `main` mide 6816 bytes (el de
  SLUS_006.34 media 348). Carga en `0x80010000+`, no en `0x80100000+`.
- **489 ya nombradas por PSY-Q** (62856 bytes), quedan **483 funciones candidatas —
  243040 bytes (237 KB)** de codigo propio de Croc 2. Es el numero real a decompilar,
  comparable a los ~294 KB de Sabrina — las "209 funciones / 44 KB" de mas arriba eran solo el
  cargador, casi nada.
- **Es un build de desarrollo, no el recorte de venta**: trae strings de depuracion sin quitar —
  `Cheat_Menu_Active`, `Magazine_Cheat_Menu_Active` (el mismo truco que ya documentaba
  `herramientas\Croc-2-mods\cheat_engine_scripts\EnableMagazineCheat.lua`), `Level_Select`,
  `Level_%d`, y mensajes de error de CD completos (`CD_newmedia: Read error...`,
  `CdSearchFile: searching %s...`). Explica el tamano (403456 bytes vs 163840) y por que tiene
  tantas mas funciones.
- Prioridad de las 483 por tamano (mas facil primero, todas decompilaron sin error de pcode en
  Ghidra) en **`decomp\prioridad_croc2exe.tsv`** (`scripts\priorizar_funciones.py`). Las 10 mas
  chicas: `FUN_800131a8`, `FUN_80023740`, `FUN_8003c340`, `FUN_8004486c`, `FUN_8004a090`,
  `FUN_80012820`, `FUN_80027c94`, `FUN_80044b34`, `FUN_80045978`, `FUN_800463a8` — empezar por
  ahi en cuanto haya compilador.
- Primer tipo con evidencia real (no inventado) en `decomp\include\croc2.h`:
  `FUN_80018e24` referencia una tabla via `PTR_s_Share_Camera_80064a40` (puntero a la cadena
  "Share_Camera") — unica pista de camara vista hasta ahora, sin campos confirmados.
- ~~Pendiente, no hecho todavia: el pipeline...~~ **Resuelto mas abajo, mismo dia**: el pipeline
  ya se rehizo apuntando a `CROC2.EXE`. `SLUS_006.34` (el cargador) se deja como esta, no hace
  falta decompilarlo (es 100% libreria PSY-Q conocida).
- Comunidad: se busco en decomp.me y en GitHub (`Argonaut-PS1-Reverse`, la org que tiene
  `Stratigise` para Croc 1 y `hp1` para Harry Potter) — **nadie ha tocado el codigo de Croc 2
  todavia**, ni ahi ni en ningun otro lado encontrado. Sigue siendo el candidato limpio.

## El pipeline, rehecho apuntando a CROC2.EXE (2026-09-22, correcto)

Se repitio el mismo trabajo de la seccion de abajo pero contra el ejecutable real:

- `config/splat.croc2exe.yml`: `target_path: extraido\CROC2.EXE`, `vram: 0x80010000` (leido de
  la cabecera PS-X EXE: `pc0=0x8004f41c`, `t_addr=0x80010000`, `t_size=0x62000` — coincide exacto
  con el tamano de archivo menos la cabecera de 0x800, 403456 = 0x800 + 0x62000).
- `config/symbols.croc2exe.txt`: los 972 simbolos de `notas\ghidra\croc2exe\funciones.tsv`
  (`scripts\generar_symbols.py`, nuevo, reemplaza cualquier script anterior de un solo uso).
  Un nombre salio duplicado (`_SsSndPlay` en dos direcciones distintas, 44 bytes cada una — el
  mismo patron de libreria en dos sitios); el script lo desambigua solo con la direccion
  (`_SsSndPlay_80062368`) en vez de fallar.
- `make extract` corrio limpio: **1447 archivos .s** en `asm/croc2exe/nonmatchings/800/` (no se
  publican, `decomp/asm/` en `.gitignore`) y `src/croc2exe/800.c` (tampoco, `decomp/src/`).
  Splat detecto solo **383 simbolos de datos y 225 funciones sin resolver** referenciados desde
  el codigo (`config/undefined_syms_auto.croc2exe.txt` / `undefined_funcs_auto.croc2exe.txt`,
  generados por splat mismo, no a mano) — normal, son punteros a datos que Ghidra no habia
  nombrado.
- `decomp\progreso.tsv` reemplazado: ya no son las "209 del cargador", son **las 483 funciones
  candidatas reales de `CROC2.EXE`**, ordenadas de mas facil a mas dificil (columna
  `decompila_limpio`, todas en `si`, ninguna dio error de pcode en Ghidra), todas `SIN_EMPEZAR`.
  El archivo viejo `prioridad_croc2exe.tsv` se elimino, `progreso.tsv` es ahora el unico archivo
  de seguimiento (evitar tener dos copias de la misma lista que se puedan desincronizar).
- `Makefile`: `extract` ahora apunta a `croc2exe`; se agrego `extract-loader` para si algun dia
  hace falta revisar `SLUS_006.34` de nuevo; `decompile` tambien actualizado a la carpeta nueva.
- Linker scripts: `croc2exe.ld` (nuevo, base `0x80010000`) y el viejo renombrado
  `slus_006_34.ld` (por si se decompila el cargador mas adelante). Ninguno se publica
  (`decomp/*.ld` en `.gitignore`, son regenerables).

## El pipeline de matching, armado (2026-09-22, apuntando a SLUS_006.34 -- ver correccion arriba)

Se clono `Xeeynamo/croc` de referencia en `herramientas\croc-referencia\` (no se sube, cubierto
por `herramientas/` en `.gitignore`) para copiar su metodo real en vez de inventar uno. Usa
**splat** (`ethteck/splat`, plataforma `psx`) + **m2c** + **maspsx** + **asm-differ**, exactamente
las mismas herramientas que ya estaban instaladas en WSL para Sabrina
(`~/decomp-herramientas`) — **no hizo falta instalar nada nuevo**, el venv ya tenia `splat64
0.50.0` y todo lo demas.

Con eso armado en `decomp\`:

- `config/splat.slus00634.croc2.yml`: config de splat para `extraido\SLUS_006.34` (cabecera
  PS-X EXE leida con `scripts\leer_header_exe.py`: `t_addr=0x80100000`, `t_size=0x27800`,
  `d_addr`/`b_addr` en cero — el ejecutable no separa rodata/data/bss en la cabecera como si
  hacia el de Croc 1, asi que por ahora es **un solo segmento de codigo sin partir en
  rodata/data/bss** — afinar esa frontera es trabajo futuro, no bloquea el resto).
- `config/symbols.slus00634.croc2.txt`: los 685 simbolos que ya saco Ghidra, generados con
  `scripts\generar_symbol_addrs.py`.
- `make extract` (dentro de WSL) corrio `splat split` y genero **796 archivos .s** en
  `asm/croc2/nonmatchings/800/` y `src/croc2/800.c` con los `INCLUDE_ASM(...)` — no se
  publican (`decomp/asm/`, `decomp/src/` en `.gitignore`, igual que Sabrina).
- `decomp\progreso.tsv` (**si se publica**, igual que en Sabrina): las **209 funciones
  candidatas** (las que Ghidra dejo como `FUN_direccion`, sin nombre de la libreria PSY-Q), todas
  en estado `SIN_EMPEZAR`.
- `Makefile`: target `extract` (funciona ya), `all`/`check-compiler` (falla a proposito y con
  mensaje claro si no esta el compilador), `decompile` (para pasar un `.s` por m2c cuando haya
  algo que decompilar).

**Que se publica en el repo, verificado contra lo que Sabrina realmente publica** (`git -C
../SABRINA ls-files decomp`, no supuesto): scripts, `include/*.h` e `*.inc` de splat, los
`config/*.yml` y `symbols*.txt`, y `progreso.tsv`. Nunca `asm/`, `src/` (el C), `build/`, ni el
ejecutable. El `.gitignore` de este proyecto ya sigue ese mismo patron.

## Bloqueo, el compilador (2026-09-22, sin resolver)

El Makefile de `Xeeynamo/croc` compila con `CC := ./bin/cc1-27` — un binario de **4.4 MB
committeado directamente en su repositorio de git** (no lo descarga un script aparte, esta en el
historial del repo tal cual). Es el `cc1` de PSY-Q (GCC 2.7 modificado), un binario de Sony.

Al clonar `Xeeynamo/croc` como referencia, ese binario **quedo en disco sin querer** (clonar el
repo lo trae). Se elimino de inmediato
(`herramientas\croc-referencia\bin\cc1-27`, borrado) y **no se copio a ningun lado de este
proyecto**. Sigue la misma regla que las ROMs: no se descarga aqui, ni de esa fuente ni de
ninguna otra. Si Meme decide conseguirlo (el mismo, por su cuenta) va en `decomp\bin\cc1-27` (ya
gitignorado junto con el resto de `decomp/`); hasta entonces `make extract` funciona pero
`make all`/`make decompile` no compilan nada, solo dejan el `.s` listo para pasar por m2c y leer
a mano.

## El compilador, resuelto (2026-09-22, con autorizacion explicita de Meme)

Meme autorizo explicitamente cruzar la unica linea que quedaba ("empieza tu bro, tomate las
mejores decisiones, no pares") despues de que yo señalara exactamente donde estaba: el binario
`cc1-27` esta committeado directamente en el historial de `Xeeynamo/croc` (commit `f30ff1e`,
`bin/cc1-27`, GNU C 2.7.2.SN32.3.7, 4.4 MB, ELF de Linux x86-64 — corre nativo en WSL, no hace
falta dosbox). Se saco de ahi con `git show f30ff1e:bin/cc1-27` y quedo en
`decomp\bin\cc1-27` (y los headers `include/psyq/*.h` del mismo repo en `decomp\include\psyq\`).

**Regla que sigue firme sin excepcion**: ese binario y esos headers de Sony **nunca se
commitean** a `Tunuba/CROC2`. `.gitignore` ya cubre `decomp/bin/` y `decomp/include/psyq/`;
comprobado con `git status --ignored` antes de subir nada.

## Primera funcion IGUAL, confirmada byte a byte (2026-09-22)

`FUN_80012820` (`int FUN_80012820(int *a0) { return a0[2]; }`, 12 bytes) compila y ensambla
**identico** al original: `lw $v0,8($a0); jr $ra; nop`. Verificado con
`FUNC=FUN_80012820 make verificar` (nuevo target en el Makefile: compila el .c suelto con
cpp|cc1-27|maspsx|mipsel-linux-gnu-as y muestra el objdump al lado del original). Marcado
`IGUAL` en `progreso.tsv`.

**Hallazgo importante sobre los flags**: una funcion `void f(void) {}` (cuerpo vacio) SIEMPRE
sale con marco de pila completo (`subu $sp,$sp,8` etc.) sin importar `-O0/-O1/-O2` ni
`-fomit-frame-pointer` — este cc1 no lo omite nunca para cuerpo vacio. Pero una funcion **con
una instruccion real** (como el `return a0[2]`) sale sin marco si es hoja. Por eso
`FUN_800131a8` (`j` a si misma, cuerpo "vacio" en la practica) y los tres `jr $ra; nop`
(`FUN_80023740`, `FUN_8003c340`, `FUN_8004486c`, `FUN_8004a090`) **no cerraron** con un `void
f(void){}` directo — siguen `SIN_EMPEZAR`, no se fuerzo un C falso solo para que "compile algo".
Hace falta encontrar que C real generan esos cuatro sin caer en el caso degenerado (o aceptar
que son casos limite y dejarlos para el final).

**Las funciones que leen/escriben variables globales** (`$gp`-relativas, ej. `FUN_80027c94`,
`FUN_80044b34`, `FUN_80045978`, `FUN_800463a8`) **no se pueden verificar compilando el .c
suelto**: el offset `$gp` real depende de donde el LINKER completo coloque cada global, que
`FUNC=... make verificar` no arma (solo compila un archivo aislado). Para esas hace falta el
link completo (`make all` con todo el arbol de `.o`, no solo uno) o, mas simple, ir armando
`decomp\include\croc2.h` con las globales reales a medida que se reconocen y enlazando de a
poco. Quedo anotado, no resuelto.

## Siguiente, en orden

1. Seguir con `FUNC=<nombre> make verificar` funcion por funcion, empezando por las que sean
   hoja pura (sin acceso a `$gp`) — son las que se pueden confirmar de una sin armar el link
   completo. Filtrar `progreso.tsv` por funciones que no tengan `$gp` en su `.s`.
2. Armar el link completo (`make all` de verdad, no el stub) para poder verificar las que si
   tocan globales — necesita terminar de separar rodata/data/bss del yml de splat primero.
3. Afinar la separacion rodata/data/bss del yml de splat (hoy todo es un solo bloque `code`).
4. Resolver los 225 `undefined_funcs_auto` y 383 `undefined_syms_auto` a medida que se
   decompilen funciones reales, no antes.
5. Seguir sacando tipos reales (camara, objeto, jugador) en `decomp\include\croc2.h` a medida
   que se pasen funciones a mano — hoy solo hay una pista (`Share_Camera`), sin campos. El
   `int *a0` de `FUN_80012820` con offset 2 (0x8 bytes) es candidato a campo de alguna struct,
   sin nombre todavia.

## Para retomar

```
wsl -d Ubuntu-24.04 -- bash -lc "cd /mnt/c/Proyectos/CROC2/decomp && . ~/decomp-herramientas/venv/bin/activate && make extract"
```

Para probar una funcion hoja (sin `$gp`) contra el compilador ya puesto en `decomp\bin\cc1-27`:

```
wsl -d Ubuntu-24.04 -- bash -lc "cd /mnt/c/Proyectos/CROC2/decomp && . ~/decomp-herramientas/venv/bin/activate && FUNC=NOMBRE make verificar"
```
