// Exporta lo que Ghidra entendio del ejecutable, para leerlo sin abrir la ventana de Ghidra.
// Uso (headless): -postScript ExportarTodo.java <carpeta_salida>
// Deja en la carpeta
//   funciones.tsv     direccion, tamano, nombre de cada funcion
//   textos.tsv        direccion de cada texto, el texto y las funciones que lo usan
//   decompilado.c     todas las funciones decompiladas a C
//@category Sabrina
import java.io.File;
import java.io.PrintWriter;

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.symbol.Reference;

public class ExportarTodo extends GhidraScript {
    @Override
    protected void run() throws Exception {
        String[] args = getScriptArgs();
        File dir = new File(args.length > 0 ? args[0] : ".");
        dir.mkdirs();

        try (PrintWriter f = new PrintWriter(new File(dir, "funciones.tsv"), "UTF-8")) {
            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            while (it.hasNext()) {
                Function fn = it.next();
                f.printf("%s\t%d\t%s%n", fn.getEntryPoint(), fn.getBody().getNumAddresses(), fn.getName());
            }
        }

        try (PrintWriter t = new PrintWriter(new File(dir, "textos.tsv"), "UTF-8")) {
            DataIterator it = currentProgram.getListing().getDefinedData(true);
            while (it.hasNext()) {
                Data d = it.next();
                if (!d.hasStringValue()) continue;
                StringBuilder quien = new StringBuilder();
                for (Reference r : getReferencesTo(d.getAddress())) {
                    Function fn = getFunctionContaining(r.getFromAddress());
                    quien.append(fn != null ? fn.getName() : "?").append('@').append(r.getFromAddress()).append(' ');
                }
                String v = String.valueOf(d.getValue()).replace("\t", "\\t").replace("\n", "\\n");
                t.printf("%s\t%s\t%s%n", d.getAddress(), v, quien.toString().trim());
            }
        }

        DecompInterface dec = new DecompInterface();
        dec.openProgram(currentProgram);
        int n = 0;
        try (PrintWriter c = new PrintWriter(new File(dir, "decompilado.c"), "UTF-8")) {
            FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
            while (it.hasNext() && !monitor.isCancelled()) {
                Function fn = it.next();
                DecompileResults r = dec.decompileFunction(fn, 60, monitor);
                c.printf("// ==== %s @ %s%n", fn.getName(), fn.getEntryPoint());
                if (r != null && r.decompileCompleted()) {
                    c.println(r.getDecompiledFunction().getC());
                } else {
                    c.println("// no se pudo decompilar");
                }
                n++;
            }
        }
        dec.dispose();
        println("ExportarTodo: " + n + " funciones en " + dir);
    }
}
