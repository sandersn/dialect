package de.tuebingen.rparse.ui;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

import javax.swing.SwingUtilities;
import javax.xml.parsers.ParserConfigurationException;

import de.tuebingen.rparse.tree.TreeException;
import de.tuebingen.rparse.tree.TreebankProcessor;
import de.tuebingen.rparse.tree.TreebankProcessorFactory;
import de.tuebingen.rparse.tree.UnknownFormatException;

public class Treeconv {

    public final static String VERSION = "unreleased";
    public final static String APP     = "treeconv - an tool for treebank format conversion.\n"
        + "More information at http://www.sfs.uni-tuebingen.de/~wmaier/treeconv.\n\n";
    public static int verbose = 0;

    public static CommandLineOptions processCommandLine(String[] cmdline) {
        CommandLineOptions op = new CommandLineOptions();
        op.add(CommandLineOptions.Prefix.DASH, "h", CommandLineOptions.Separator.BLANK, false, "Show help");
        op.add(CommandLineOptions.Prefix.DASH, "z", CommandLineOptions.Separator.BLANK, false, "Start the GUI");
        op.add(CommandLineOptions.Prefix.DASH, "v", CommandLineOptions.Separator.BLANK, true, "Verbose level");
        op.add(CommandLineOptions.Prefix.DASH, "i", CommandLineOptions.Separator.BLANK, true, "Input format");
        op.add(CommandLineOptions.Prefix.DASH, "o", CommandLineOptions.Separator.BLANK, true, "Output format");
        op.add(CommandLineOptions.Prefix.DASH, "c", CommandLineOptions.Separator.BLANK, true, "Input corpus");
        op.add(CommandLineOptions.Prefix.DASH, "t", CommandLineOptions.Separator.BLANK, true, "Transformed corpus");
        op.add(CommandLineOptions.Prefix.DASH, "s", CommandLineOptions.Separator.BLANK, true, "Interval start");
        op.add(CommandLineOptions.Prefix.DASH, "e", CommandLineOptions.Separator.BLANK, true, "Interval end");
        op.prepare();
        String line = "";
        for (int i = 0; i < cmdline.length; i++) {
            String tmp = cmdline[i];
            tmp = tmp.replace(" ", "---");
            line += "\"" + tmp + "\" ";
        }
        op.parse(line);
        return op;
    }

    public static String usage() {
        String ret = APP;
        ret += "Usage (asterisks mark default values):\n";
        ret += "treeconv OPTIONS, where OPTIONS is one or more of:\n";
        ret += "         -h                     : show this message\n";
        ret += "         -v [level]             : set verbose level\n";
        ret += "         -c [treebank]          : input treebank\n";
        ret += "         -i [format]            : input treebank format\n";
        ret += "         -t [treebank]          : transformed treebank\n";
        ret += "         -o [format]            : transformed treebank format\n";
        ret += "         -s [sentnum]           : start processing at sentence sentnum\n";
        ret += "         -e [sentnum]           : end processing at sentence sentnum\n";
        ret += "         -z                     : start the GUI.\n\n";
        ret += "In case one of the parameters -c, -i, -t, -o is missing, the GUI is started.\n";
        return ret;
    }
    
    public static String version() {
        return APP + VERSION + "\n";
    }

    public static void main(String[] args) {
        CommandLineOptions op = processCommandLine(args);
        if (op.check("h")) {
            System.out.println(usage());
            System.exit(0);
        }
        if ((!(op.check("c") && op.check("i") && op.check("t") && op.check("o")))
                || op.check("z")) {
            op.setVal("v", "\"" + "\"");
            final CommandLineOptions finalop = op;
            SwingUtilities.invokeLater(new Runnable() {
                public void run() {
                    new TreeconvGui(finalop);
                }
            });
        } else {
            try {
                doTransform(op);
            } catch (FileNotFoundException e) {
                System.err.println("File not found: " + e.getMessage());
            } catch (IOException e) {
                System.err.println("IO Exception: " + e.getMessage());
            } catch (UnknownFormatException e) {
                System.err.println("Unknown Format: " + e.getMessage());
            } catch (TreeException e) {
                System.err.println("Tree transformation problem: "
                        + e.getMessage());
            } catch (ParserConfigurationException e) {
                System.err.println("Could not configure XML parser: "
                        + e.getMessage());
            }
        }
    }

    public synchronized static void doTransform(CommandLineOptions op)
            throws IOException, UnknownFormatException, TreeException, ParserConfigurationException {
        String intreebank = op.getVal("c");
        String informat = op.getVal("i");
        String outtreebank = op.getVal("t");
        String outformat = op.getVal("o");
        int from = -1;
        if (op.check("s")) {
            try {
                from = Integer.parseInt(op.getVal("s"));
            } catch (NumberFormatException e) {
            }
        }
        int to = -1;
        if (op.check("e")) {
            try {
                to = Integer.parseInt(op.getVal("e"));
            } catch (NumberFormatException e) {
            }
        }
        File outfile = new File(outtreebank);
        if (!op.check("v")) 
            verbose = 0;
        if (op.check("v")) {
            System.err.println("Set input format to " + informat + ".\nSet output format to " + outformat + ".");
            if (from != -1 || to != -1) {
                System.err.print("Processing interval: From ");
                if (from == -1) {
                    System.err.print("start");
                } else {
                    System.err.print(from);
                }
                System.err.print(" to ");
                if (to == -1) {
                    System.err.print("end");
                } else {
                    System.err.print(to);
                }
                System.err.println();
            }
            System.err.println("Transforming treebank at " + intreebank + " to " + outtreebank + "...");
        }
        System.err.flush();
        TreebankProcessor tt = TreebankProcessorFactory.getTreebankProcessor(intreebank, informat, from, to, verbose);
        tt.transformTreebank(outfile, outformat);
        if (op.check("v"))
            System.err.println("done.\n");
    }

}
