/* Enlazado minimo para verificar UNA funcion en SU direccion real (necesario para que un
   salto tipo j/jal a una etiqueta propia, ej. un loop "j si_mismo", salga con los mismos
   bits que el original). La direccion se da directo en la seccion (no con ". = ADDR;") para
   que el linker no la vuelva a alinear a los 16 bytes que pide .text por defecto y la corra. */
SECTIONS
{
    .text 0x90000000 : { *(.text) }
    .rodata : { *(.rodata) }
    .data : { *(.data) }
    .bss : { *(.bss) }
    /DISCARD/ : { *(.comment) *(.mdebug*) *(.pdr) *(.gnu.attributes) *(.reginfo) *(.MIPS.abiflags) }
}
