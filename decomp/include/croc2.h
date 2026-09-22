// Tipos y notas de CROC2.EXE, el ejecutable real del juego (ver notas/TRASPASO.md).
// Solo lo que se ve confirmado en el codigo o en los strings de depuracion del disco.
// No hay todavia una struct de camara/jugador/objeto confirmada por campos: falta pasar
// funciones a mano de decomp/prioridad_croc2exe.tsv para sacarla con evidencia real.

#ifndef CROC2_H
#define CROC2_H

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
