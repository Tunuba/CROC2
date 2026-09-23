// Tipos y notas de CROC2.EXE, el ejecutable real del juego (ver notas/TRASPASO.md).
// Solo lo que se ve confirmado en el codigo o en los strings de depuracion del disco.
// No hay todavia una struct de camara/jugador/objeto confirmada por campos: falta pasar
// funciones a mano de decomp/prioridad_croc2exe.tsv para sacarla con evidencia real.

#ifndef CROC2_H
#define CROC2_H

// Convencion estandar de la comunidad de decomp (no es de PSY-Q, PSY-Q no trae esto):
// tipos de ancho fijo cortos para que el C generado por m2c compile tal cual.
typedef signed char s8;
typedef unsigned char u8;
typedef short s16;
typedef unsigned short u16;
typedef int s32;
typedef unsigned int u32;
typedef long long s64;
typedef unsigned long long u64;
typedef float f32;
typedef double f64;

// CROC2.EXE es un build de desarrollo, no uno recortado para venta: trae menu de trucos
// ("Cheat_Menu_Active", "Magazine_Cheat_Menu_Active" -- el mismo truco que documenta
// hdc0/Croc-2-mods/cheat_engine_scripts/EnableMagazineCheat.lua), selector de nivel
// ("Level_Select", "Level_%d") y mensajes de error de CD sin recortar
// ("CD_newmedia: Read error...", "CdSearchFile: searching %s..."). Esto explica por que
// pesa mas del doble que SLUS_006.34 y tiene 972 funciones contra 685.
//
// FUN_80018e24 referencia una tabla via PTR_s_Share_Camera_80064a40 (un puntero a la
// cadena "Share_Camera"): es la unica pista de camara vista hasta ahora, sin campos
// confirmados todavia.

#endif
