package de.tuebingen.rparse.ui;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.regex.PatternSyntaxException;

/*
 * Class for command line options processing freely inspired by : Dr. Matthias Laux
 * (http://www.javaworld.com/javaworld/jw-08-2004/jw-0816-command.html)
 */
public class CommandLineOptions {

    // Enumerate the different components of a command line

    // 1. A prefix (default is -)
    public enum Prefix {
        DASH('-'), SLASH('/');

        private char c;
        private Prefix(char c) {
            this.c = c;
        }
        char getName() {
            return c;
        }
    }

    // 2. A separator (default is blank)
    public enum Separator {
        BLANK(' '), COLON(':'), EQUALS('='), NONE('D');

        private char c;
        private Separator(char c) {
            this.c = c;
        }
        char getName() {
            return c;
        }
    }

    // Define an option
    class Option {

        private Prefix    prefix;
        private String    key;
        private Separator sep;
        private boolean   needsVal;
        private String    descr;

        Option(Prefix prefix, String key, Separator separator, boolean value,
                String descr) {
            this.prefix = prefix;
            this.key = key;
            this.sep = separator;
            this.needsVal = value;
            this.descr = descr;
        }

        Prefix getPrefix() {
            return prefix;
        }

        void setPrefix(Prefix prefix) {
            this.prefix = prefix;
        }

        String getKey() {
            return key;
        }

        void setKey(String key) {
            this.key = key;
        }

        Separator getSep() {
            return sep;
        }

        void setSep(Separator sep) {
            this.sep = sep;
        }

        boolean getNeedsVal() {
            return needsVal;
        }

        void setNeedsVal(boolean needsVal) {
            this.needsVal = needsVal;
        }

        String getDescr() {
            return descr;
        }

        void setDescr(String descr) {
            this.descr = descr;
        }

    }

    private List<Option>               options;
    private Hashtable<String, Pattern> patterns;
    private Hashtable<String, String>  values;
    private Hashtable<String, Option>  optionmap;

    public CommandLineOptions() {
        options = new LinkedList<Option>();
        patterns = new Hashtable<String, Pattern>();
        values = new Hashtable<String, String>();
        optionmap = new Hashtable<String, Option>();
    }

    public void merge(CommandLineOptions localOps) {
        Iterator<String> it = localOps.getValues().keySet().iterator();
        while (it.hasNext()) {
            String localKey = it.next();
            setOurVal(localKey, localOps.getVal(localKey));
        }
    }

    public void add(Prefix prefix, String key, Separator separator,
            boolean value, String descr) {
        Option o = new Option(prefix, key, separator, value, descr);
        options.add(o);
        optionmap.put(key, o);
    }

    /**
     * Prepare the parsers for each possible option
     */
    public void prepare() {
        String accents = "\u00e9\u00e8\u00ea\u00f9\u00fb\u00fc\u00f4\u00ee\u00ef\u00e2\u00c0\u00f6\u00e4"; // éèêùûüôîïâàöä

        for (int i = 0; i < options.size(); i++) {
            Option o = options.get(i);
            Prefix prefix = o.getPrefix();
            String key = o.getKey();
            Separator sep = o.getSep();
            boolean needsVal = o.getNeedsVal();
            Pattern p;
            if (needsVal) {
                p = java.util.regex.Pattern.compile("\"" + prefix.getName()
                        + key + "\"" + sep.getName() + "([\\p{Punct}\"a-zA-Z"
                        + accents + "0-9\\.\\@_\\" + File.separator + "~-]+)");
            } else {
                p = java.util.regex.Pattern.compile("\"" + prefix.getName()
                        + key + "\"()");
            }
            patterns.put(key, p);
        }
    }

    /**
     * Process the command line to find the options
     */
    public void parse(String line) {
        Set<String> keys = patterns.keySet();
        Iterator<String> i = keys.iterator();
        while (i.hasNext()) {
            String k = (String) i.next();
            Pattern p = patterns.get(k);
            // try this option on the command line
            try {
                Matcher m = p.matcher(line);
                boolean a = m.find();
                if (a) {
                    // System.err.println("-- "+k+": "+m.group(1));
                    values.put(k, m.group(1));
                }
                //else { System.err.println("Line : "+line); System.err.println("Pattern not found : "+p.pattern()); }
            } catch (PatternSyntaxException pse) {
                System.err.println(pse.getDescription());
            } catch (IllegalStateException ise) {
                System.err.println(ise.toString());
            }
            // next option
        }
    }

    public Enumeration<String> getKeys() {
        return values.keys();
    }

    public Hashtable<String, String> getValues() {
        return values;
    }

    public Integer getNumVal(String key) {
        Integer ret = null;
        if (values.containsKey(key)) {
            String res = values.get(key);
            // System.out.println(res);
            if (res.length() > 0) {
                res = res.replace("---", " ");
                // we remove the ""
                try {
                    ret = Integer.valueOf(res.substring(1, (res.length() - 1)));
                } catch (NumberFormatException e) {} 
            } else {
                try {
                    ret = Integer.valueOf(res.substring(1, (res.length() - 1)));
                } catch (NumberFormatException e) {} 
            }
        } else {
            return null;
        }
        return ret;
    }

    public String getVal(String key) {
        if (values.containsKey(key)) {
            String res = values.get(key);
            // System.out.println(res);
            if (res.length() > 0) {
                res = res.replace("---", " ");
                // we remove the ""
                return res.substring(1, (res.length() - 1));
            } else
                return res;
        } else {
            return null;
        }
    }

    public String getDescr(String key) {
        String ret = "";
        if (values.containsKey(key))
            ret = optionmap.get(key).getDescr();
        return ret;
    }

    public void removeAll() {
        values.clear();
    }

    public void removeVal(String key) {
        values.remove(key);
    }

    public void setOurVal(String key, String value) {
        values.put(key, "\"" + value + "\"");
    }

    public void setVal(String key, String value) {
        values.put(key, value);
    }

    public boolean check(String key) {
        return (values.containsKey(key));
    }

    public String toString() {
        String res = "";
        for (String k : values.keySet()) {
            if (values.get(k).equals(""))
                res += k + "\n";
            else
                res += k + " -> " + values.get(k) + "\n";
        }
        return res;
    }

    /*
     * options <-> config files
     */
    public static CommandLineOptions getConfigFromFile(File cf) {
        CommandLineOptions ret = new CommandLineOptions();
        return ret;
    }

    public void writeConfigToFile(File cf) throws IOException {
        BufferedWriter bw = new BufferedWriter(new FileWriter(cf));
        for (String k : values.keySet()) {
            if (values.get(k).equals("")) {
                bw.write("%" + getDescr(k) + "\n");
                bw.write(k + "\n");
            } else {
                bw.write("%" + getDescr(k) + "\n");
                bw.write(k + " --> " + getVal(k) + "\n");
            }
        }
        bw.close();
        System.err.println("Config written to " + cf.getAbsolutePath());
    }

}
