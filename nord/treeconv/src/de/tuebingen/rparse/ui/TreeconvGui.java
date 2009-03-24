package de.tuebingen.rparse.ui;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.io.File;
import java.io.FileNotFoundException;

import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JRadioButton;
import javax.swing.JScrollPane;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.WindowConstants;
import javax.swing.border.EmptyBorder;
import javax.swing.border.TitledBorder;

import de.tuebingen.rparse.tree.ui.TreeViewer;

public class TreeconvGui extends AbstractGui implements ActionListener {

    private int                 verbose              = 0;

    public final static int    TF_W                 = 300;
    public final static int    OPT_W                = 30;
    public final static int    OPT_H                = 25;

    private final static String RUN                  = "Run";
    private final static String TREEVIEWER_INPUT     = "Start tree viewer for input file";
    private final static String CHOOSE_INPUTFILE     = "Choose Inputfile";
    private final static String CHOOSE_INFORMATOPTS  = "Choose Input Format Options";
    private final static String CHOOSE_OUTPUTFILE    = "Choose Outputfile";
    private final static String CHOOSE_OUTFORMATOPTS = "Choose Output Format Options";
    private final static String CHOOSE_GRAMMARDIR    = "Choose Grammarfile";
    private final static String CHOOSE_GRAMMAROPTS   = "Choose Grammar Format Options";
    private final static String QUIT                 = "Quit";
    private final static String TOGGLE_SHELL         = "Toggle shell";
    private final static String CLEAR_SHELL          = "Clear shell";
    private final static String SET_VERBOSE          = "Set Verbose Level";
    private final static String ABOUT                = "About";

    private Thread              gt;
    private CommandLineOptions  op;
    private File                curPath;

    private JButton             inputViewButton;
    
    private File                infile;
    private GuiDialog           infD;
    private JTextField          infileF;
    private JComboBox           informatF;
    private JTextField          fromF;
    private JTextField          toF;
    private String[]            informats = {"export", "brackets", "brackets-indent", "tiger-xml"};

    // private JTabbedPane outputmodepane;

    private File                outfile;
    private JTextField          outfileF;
    private JComboBox           outformatF;
    private String[]            outformats = {"export", "brackets", "brackets-indent", "tiger-xml", "terminals", "none"};
    private GuiDialog           outfD;
    private JCheckBox           out_nopunctB;
    private JCheckBox           out_vrootB;
    private JCheckBox           out_splitoutB;

    private File                grammarfile;
    private JTextField          grammarF;
    private JComboBox           grammarformatF;
    private String[]            grammarformats = {"lopar/bitpar", "rparse"};

    private JButton             runButton;

    private JRadioButton        onelinesentbut;
    private JRadioButton        onelinewordbut;
    private JCheckBox           includepostagsB;
    private JTextField          tagseparatorF;

    public TreeconvGui(CommandLineOptions op) {
        super("treeconv");
        this.op = op;
        this.gt = new Launcher(this);
        getMainFrame().setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        getMainFrame().add(mainPanel());
        getMainFrame().setLocationRelativeTo(null);
        getMainFrame().pack();
        getMainFrame().setVisible(true);
        getShellFrame().setSize(500, 300);
        getShellFrame().setMinimumSize(new Dimension(100, 100));
        getShellFrame().setLocationRelativeTo(null);
        getShellFrame().add(shellPanel());
        getShellFrame().setVisible(false);
    }

    public JMenuBar menuBar() {
        JMenuBar ret = new JMenuBar();
        // File
        JMenu menu = new JMenu("File");
        menu.setMnemonic('f');
        JMenuItem m = new JMenuItem(QUIT);
        m.setActionCommand(QUIT);
        m.setMnemonic(KeyEvent.VK_Q);
        m.addActionListener(this);
        menu.add(m);
        ret.add(menu);
        // View
        menu = new JMenu("View");
        menu.setMnemonic('v');
        m = new JMenuItem(TOGGLE_SHELL);
        m.setActionCommand(TOGGLE_SHELL);
        m.setMnemonic(KeyEvent.VK_T);
        m.addActionListener(this);
        menu.add(m);
        ret.add(menu);
        // Config
        menu = new JMenu("Config");
        menu.setMnemonic('c');
        m = new JMenuItem(SET_VERBOSE);
        m.setActionCommand(SET_VERBOSE);
        m.setMnemonic(KeyEvent.VK_V);
        m.addActionListener(this);
        menu.add(m);
        // ret.add(menu);
        // ?
        menu = new JMenu("?");
        menu.setMnemonic('?');
        m = new JMenuItem(ABOUT);
        m.setActionCommand(ABOUT);
        m.setMnemonic(KeyEvent.VK_A);
        m.addActionListener(this);
        menu.add(m);
        ret.add(menu);
        return ret;
    }

    public void infDialog() {
        JPanel infDContentPanel2 = new JPanel();
        infDContentPanel2.setLayout(new BoxLayout(infDContentPanel2,
                BoxLayout.PAGE_AXIS));

        JPanel infpanel = new JPanel();
        infpanel.setLayout(new BoxLayout(infpanel, BoxLayout.PAGE_AXIS));
        JPanel fromtoPanel = new JPanel();
        fromtoPanel.setLayout(new BoxLayout(fromtoPanel, BoxLayout.LINE_AXIS));
        fromtoPanel.setBorder(new TitledBorder("Processing interval"));
        fromtoPanel.add(new JLabel(" Sentences "));
        fromF = new JTextField();
        fromF.setPreferredSize(new Dimension(OPT_W, OPT_H));
        fromtoPanel.add(fromF);
        fromtoPanel.add(new JLabel(" to "));
        toF = new JTextField();
        toF.setPreferredSize(new Dimension(OPT_W, OPT_H));
        fromtoPanel.add(toF);
        fromtoPanel.add(new JLabel(" "));
        infpanel.add(fromtoPanel);
        infDContentPanel2.add(infpanel);

        infD = new GuiDialog();
        JPanel infDContentPanel = new JPanel(new BorderLayout());
        infDContentPanel.add(infDContentPanel2, BorderLayout.CENTER);
        JPanel closeButtonPanel = new JPanel();
        JButton closeButton = new JButton("OK");
        closeButton.addActionListener(infD);
        closeButtonPanel.setBorder(new EmptyBorder(6, 2, 2, 2));
        closeButtonPanel.add(closeButton);
        infDContentPanel.add(closeButtonPanel, BorderLayout.SOUTH);
        infDContentPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
        infD.setTitle("Input format");
        infD.setModal(true);
        infD.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE);
        infD.add(infDContentPanel);
        infD.pack();
        infD.setResizable(false);
        infD.setLocationRelativeTo(null);
    }

    public void outfDialog() {
        outfD = new GuiDialog();
        outfD.setTitle("Output format");
        outfD.setModal(true);
        outfD.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE);
        JPanel outfDContentPanel = new JPanel(new BorderLayout());

        JPanel outfDContentPanel2 = new JPanel();
        outfDContentPanel2.setLayout(new BoxLayout(outfDContentPanel2,
                BoxLayout.PAGE_AXIS));

        JPanel outfcheckboxpanel = new JPanel();
        outfcheckboxpanel.setLayout(new BoxLayout(outfcheckboxpanel,
                BoxLayout.PAGE_AXIS));
        JPanel splitoutpanel = new JPanel(new BorderLayout());
        splitoutpanel
                .add(new JLabel(" Split output in one file per sentence "));
        out_splitoutB = new JCheckBox();
        out_splitoutB.setSelected(false);
        splitoutpanel.add(out_splitoutB, BorderLayout.EAST);
        splitoutpanel.setBorder(new TitledBorder("Split output"));
        outfcheckboxpanel.add(splitoutpanel);
        JPanel outnopunctpanel = new JPanel(new BorderLayout());
        outnopunctpanel.add(new JLabel(" Remove punctuation from output "),
                BorderLayout.WEST);
        out_nopunctB = new JCheckBox();
        out_nopunctB.setSelected(false);
        outnopunctpanel.add(out_nopunctB, BorderLayout.EAST);
        outnopunctpanel.setBorder(new TitledBorder("Punctuation"));
        outfcheckboxpanel.add(outnopunctpanel);
        JPanel attachvrootpanel = new JPanel(new BorderLayout());
        attachvrootpanel.add(new JLabel(
                " 'Continuitfy' discontinuous top node "), BorderLayout.WEST);
        out_vrootB = new JCheckBox();
        out_vrootB.setSelected(false);
        attachvrootpanel.add(out_vrootB, BorderLayout.EAST);
        attachvrootpanel.setBorder(new TitledBorder("VROOT"));
        outfcheckboxpanel.add(attachvrootpanel);
        outfDContentPanel2.add(outfcheckboxpanel);

        JPanel outfterminalspanel = new JPanel(new BorderLayout());
        JLabel info = new JLabel(
                " Only available when terminal output is selected.");
        info.setBorder(new EmptyBorder(3, 1, 8, 1));
        outfterminalspanel.add(info, BorderLayout.NORTH);
        JPanel outfterminalscontentpanel = new JPanel();
        outfterminalscontentpanel.setLayout(new BoxLayout(
                outfterminalscontentpanel, BoxLayout.PAGE_AXIS));

        JPanel onelinepanel = new JPanel();
        JPanel onelinepanel2 = new JPanel();
        onelinesentbut = new JRadioButton("One line per sentence");
        onelinewordbut = new JRadioButton("One line per word");
        onelinewordbut.setSelected(true);
        ButtonGroup onelineg = new ButtonGroup();
        onelineg.add(onelinesentbut);
        onelineg.add(onelinewordbut);
        onelinepanel
                .setLayout(new BoxLayout(onelinepanel, BoxLayout.PAGE_AXIS));
        onelinepanel.add(onelinesentbut);
        onelinepanel.add(onelinewordbut);
        onelinepanel.add(onelinepanel2);
        onelinepanel.setBorder(new TitledBorder("Line distribution"));
        outfterminalscontentpanel.add(onelinepanel);

        JPanel postagpanel = new JPanel();
        JPanel postagcontentpanel = new JPanel();

        JPanel includepospanel = new JPanel(new BorderLayout());
        includepospanel.add(new JLabel(" Include GFs "), BorderLayout.WEST);
        includepostagsB = new JCheckBox();
        includepostagsB.setSelected(false);
        includepospanel.add(includepostagsB, BorderLayout.EAST);
        includepospanel.setBorder(new TitledBorder(""));
        postagcontentpanel.add(includepospanel);

        JPanel seppanel = new JPanel(new BorderLayout());
        seppanel.add(new JLabel(" Separator: "), BorderLayout.WEST);
        tagseparatorF = new JTextField();
        tagseparatorF.setPreferredSize(new Dimension(OPT_W, OPT_H));
        seppanel.add(tagseparatorF);
        postagcontentpanel.add(seppanel);

        postagpanel.add(postagcontentpanel, BorderLayout.CENTER);
        postagpanel.setBorder(new TitledBorder("GF"));
        outfterminalscontentpanel.add(postagpanel);

        outfterminalspanel.add(outfterminalscontentpanel, BorderLayout.CENTER);
        outfterminalspanel.setBorder(new TitledBorder("Terminals output"));
        outfDContentPanel2.add(outfterminalspanel);

        outfDContentPanel.add(outfDContentPanel2, BorderLayout.CENTER);

        JPanel closeButtonPanel = new JPanel();
        JButton closeButton = new JButton("OK");
        closeButton.addActionListener(outfD);
        closeButtonPanel.setBorder(new EmptyBorder(6, 2, 2, 2));
        closeButtonPanel.add(closeButton);
        outfDContentPanel.add(closeButtonPanel, BorderLayout.SOUTH);

        outfDContentPanel.setBorder(new EmptyBorder(5, 5, 5, 5));
        outfD.add(outfDContentPanel);
        outfD.pack();
        outfD.setResizable(false);
        outfD.setLocationRelativeTo(null);
    }

    public JPanel configPanel() {
        infDialog();
        JPanel input = new JPanel();
        input.setLayout(new BoxLayout(input, BoxLayout.PAGE_AXIS));
        JPanel inputfilepanel = new JPanel(new BorderLayout());
        infileF = new JTextField();
        infileF.setPreferredSize(new Dimension(TF_W, infileF.getSize().height));
        inputfilepanel.add(infileF, BorderLayout.CENTER);
        JPanel infileselectorButtonPanel = new JPanel();
        infileselectorButtonPanel.setLayout(new BoxLayout(infileselectorButtonPanel, BoxLayout.LINE_AXIS));
        JButton infileChooser = new JButton("Browse...");
        infileChooser.setActionCommand(CHOOSE_INPUTFILE);
        infileChooser.addActionListener(this);
        infileChooser.setMnemonic('b');
        infileselectorButtonPanel.add(infileChooser);
        inputViewButton = new JButton("Explore...");
        inputViewButton.setActionCommand(TREEVIEWER_INPUT);
        inputViewButton.addActionListener(this);
        inputViewButton.setMnemonic('i');
        infileselectorButtonPanel.add(inputViewButton);
        inputfilepanel.add(infileselectorButtonPanel, BorderLayout.EAST);
        inputfilepanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        JPanel inputformatpanel = new JPanel(new BorderLayout());
        inputformatpanel.add(new JLabel("Format:  "), BorderLayout.WEST);
        informatF = new JComboBox(informats);
        inputformatpanel.add(informatF, BorderLayout.CENTER);
        JButton informatoptions = new JButton("Options...");
        informatoptions.setActionCommand(CHOOSE_INFORMATOPTS);
        informatoptions.addActionListener(this);
        informatoptions.setMnemonic('o');
        inputformatpanel.add(informatoptions, BorderLayout.EAST);
        inputformatpanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        input.add(inputfilepanel);
        input.add(inputformatpanel);
        input.setBorder(new TitledBorder("Input"));

        outfDialog();
        JPanel output = new JPanel();
        output.setLayout(new BoxLayout(output, BoxLayout.PAGE_AXIS));
        JPanel outputfilepanel = new JPanel(new BorderLayout());
        outfileF = new JTextField();
        outfileF
                .setPreferredSize(new Dimension(TF_W, outfileF.getSize().height));
        outputfilepanel.add(outfileF, BorderLayout.CENTER);
        JButton outfileChooser = new JButton("Browse...");
        outfileChooser.setActionCommand(CHOOSE_OUTPUTFILE);
        outfileChooser.addActionListener(this);
        outfileChooser.setMnemonic('r');
        outputfilepanel.add(outfileChooser, BorderLayout.EAST);
        outputfilepanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        JPanel outputformatpanel = new JPanel(new BorderLayout());
        outformatF = new JComboBox(outformats);
        outputformatpanel.add(new JLabel("Format:  "), BorderLayout.WEST);
        outputformatpanel.add(outformatF, BorderLayout.CENTER);
        JButton outformatoptions = new JButton("Options...");
        outformatoptions.setActionCommand(CHOOSE_OUTFORMATOPTS);
        outformatoptions.addActionListener(this);
        outformatoptions.setMnemonic('p');
        outputformatpanel.add(outformatoptions, BorderLayout.EAST);
        outputformatpanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        output.add(outputfilepanel);
        output.add(outputformatpanel);

        JPanel grammar = new JPanel();
        grammar.setLayout(new BoxLayout(grammar, BoxLayout.PAGE_AXIS));
        JPanel grammarfilepanel = new JPanel(new BorderLayout());
        grammarF = new JTextField();
        grammarF
                .setPreferredSize(new Dimension(TF_W, grammarF.getSize().height));
        grammarfilepanel.add(grammarF, BorderLayout.CENTER);
        JButton grammarfileChooser = new JButton("Browse...");
        grammarfileChooser.setActionCommand(CHOOSE_GRAMMARDIR);
        grammarfileChooser.addActionListener(this);
        grammarfileChooser.setMnemonic('r');
        grammarfilepanel.add(grammarfileChooser, BorderLayout.EAST);
        grammarfilepanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        JPanel grammarformatpanel = new JPanel(new BorderLayout());
        grammarformatF = new JComboBox(grammarformats);
        grammarformatpanel.add(new JLabel("Format:  "), BorderLayout.WEST);
        grammarformatpanel.add(grammarformatF, BorderLayout.CENTER);
        JButton grammarformatoptions = new JButton("Options...");
        grammarformatoptions.setActionCommand(CHOOSE_GRAMMAROPTS);
        grammarformatoptions.addActionListener(this);
        grammarformatoptions.setMnemonic('p');
        grammarformatpanel.add(grammarformatoptions, BorderLayout.EAST);
        grammarformatpanel.setBorder(new EmptyBorder(2, 2, 2, 2));
        grammar.add(grammarfilepanel);
        grammar.add(grammarformatpanel);

        /*
         * outputmodepane = new JTabbedPane(); 
         * outputmodepane.setBorder(new TitledBorder("Output"));
         * outputmodepane.addTab("Corpus", null, output, "Corpus output"); 
         * outputmodepane.setMnemonicAt(0, KeyEvent.VK_C); 
         * outputmodepane.addTab("Grammar", null, grammar, "Grammar output");
         * outputmodepane.setMnemonicAt(0, KeyEvent.VK_G);
         */

        output.setBorder(new TitledBorder("Output"));

        JPanel ret = new JPanel();
        ret.setLayout(new BoxLayout(ret, BoxLayout.PAGE_AXIS));
        ret.add(input);
        // ret.add(outputmodepane);
        ret.add(output);
        ret.setBorder(new EmptyBorder(5, 5, 5, 5));
        return ret;
    }

    public JPanel actionPanel() {
        JPanel ret = new JPanel(new BorderLayout());
        runButton = new JButton(RUN);
        runButton.setActionCommand(RUN);
        runButton.addActionListener(this);
        runButton.setMnemonic('u');
        ret.add(runButton);
        ret.setBorder(new EmptyBorder(5, 5, 5, 5));
        return ret;
    }

    public JPanel mainPanel() {
        JPanel ret = new JPanel(new BorderLayout());
        ret.add(menuBar(), BorderLayout.NORTH);
        ret.add(configPanel(), BorderLayout.CENTER);
        ret.add(actionPanel(), BorderLayout.SOUTH);
        return ret;
    }

    public JPanel shellControlPanel() {
        JPanel ret = new JPanel();
        ret.setLayout(new BoxLayout(ret, BoxLayout.LINE_AXIS));
        JButton clearShellButton = new JButton(CLEAR_SHELL);
        clearShellButton.setActionCommand(CLEAR_SHELL);
        clearShellButton.addActionListener(this);
        ret.add(clearShellButton);
        ret.setBorder(new EmptyBorder(3, 3, 3, 3));
        return ret;
    }

    public JPanel shellPanel() {
        JPanel ret = new JPanel(new BorderLayout());
        getShell().setEditable(false);
        JScrollPane shellPane = new JScrollPane(getShell());
        shellPane.setPreferredSize(new Dimension(200, 200));
        ret.add(shellPane, BorderLayout.CENTER);
        ret.add(shellControlPanel(), BorderLayout.SOUTH);
        return ret;
    }

    public void about() {
        String msg = "";
        msg += "treeconv is a tool for treebank conversion.\n\n";
        msg += "This is version " + Treeconv.VERSION + "\n";
        msg += "More information at: \n";
        msg += "http://www.sfs.uni-tuebingen.de/~wmaier/treeconv";
        JOptionPane.showMessageDialog(getMainFrame(), msg);
    }

    public class Launcher extends Thread {

        private AbstractGui g;

        public Launcher(AbstractGui g) {
            this.g = g;
        }

        public synchronized void run() {
            runButton.setEnabled(false);
            boolean error = false;
            try {
                Treeconv.doTransform(op);
            } catch (FileNotFoundException e) {
                g.showError("Could not open file: " + e.getMessage());
                error = true;
            } catch (Exception e) {
                g.showError("Could not complete transformation task! Reason:\n"
                        + e.getMessage());
                error = true;
            }
            if (!error)
                g.showMessage("Transformation completed.");
            runButton.setEnabled(true);
        }

    }

    public void grabOptions() {
        op.setVal("i", "\"" + informatF.getSelectedItem() + "\"");
        String outformat = outformatF.getSelectedItem().toString();
        if (out_nopunctB.isSelected())
            outformat += "-nopunct";
        if (out_vrootB.isSelected())
            outformat += "-vroot";
        if (out_splitoutB.isSelected())
            outformat += "-split";
        if (onelinesentbut.isSelected())
            outformat += "-oneline";
        if (includepostagsB.isSelected()) {
            outformat += "-gf";
            String tagsep = tagseparatorF.getText();
            if (tagsep.length() > 0)
                outformat += "-SEP" + tagsep.charAt(0);
        }
        if (!fromF.getText().trim().equals("")) {
            try {
                Integer.parseInt(fromF.getText().trim());
                op.setVal("s", "\"" + fromF.getText().trim() + "\"");
            } catch (NumberFormatException e) {
            }
        } else {
            op.setVal("s", "\"" + "" + "\"");
        }
        if (!toF.getText().trim().equals("")) {
            try {
                Integer.parseInt(toF.getText().trim());
                op.setVal("e", "\"" + toF.getText().trim() + "\"");
            } catch (NumberFormatException e) {
            }
        } else {
            op.setVal("e", "\"" + "" + "\"");
        }
        op.setVal("o", "\"" + outformat + "\"");
        op.setVal("c", "\"" + infileF.getText() + "\"");
        op.setVal("t", "\"" + outfileF.getText() + "\"");
    }

    
    public void actionPerformed(ActionEvent e) {
        String cmd = e.getActionCommand();
        if (verbose > 1)
            System.err.println("[Gui] " + cmd);
        if (RUN.equals(cmd)) {
            grabOptions();
            gt = new Launcher(this);
            gt.run();
        } else if (TREEVIEWER_INPUT.equals(cmd)) {
            grabOptions();
            String msg = "";
            if (!op.check("c") || op.getVal("c").trim().equals("")) 
                msg += "You must specify a treebank.";
            File f = new File(op.getVal("c"));
            if (!f.exists())
                msg = "Specified treebank file does not exist.";
//            if (!("").equals(msg)) { 
//                JOptionPane.showMessageDialog(getMainFrame(), msg, "Error", JOptionPane.WARNING_MESSAGE);
//            } else {
                final CommandLineOptions finalop = op;
                SwingUtilities.invokeLater(new Runnable() {
                    public void run() {
                        new TreeViewer(finalop, getMainFrame());
                    }
                });
//            }
        } else if (CHOOSE_INPUTFILE.equals(cmd)) {
            JFileChooser jf = new JFileChooser();
            if (!infileF.getText().trim().equals(""))
                jf.setCurrentDirectory(new File(infileF.getText().trim()));
            else if (curPath != null)
                jf.setCurrentDirectory(curPath);
            jf.setDialogTitle("Please select an input corpus");
            int retval = jf.showOpenDialog(getMainFrame());
            if (retval == JFileChooser.APPROVE_OPTION) {
                File tf = jf.getSelectedFile();
                if (tf != null) {
                    infile = new File(jf.getSelectedFile().getAbsolutePath());
                    if (verbose > 2)
                        System.err.println("[Gui] Selected input file: "
                                + infile.toString());
                }
                curPath = jf.getCurrentDirectory();
                infileF.setText(infile.getAbsolutePath());
            }
        } else if (CHOOSE_INFORMATOPTS.equals(cmd)) {
            infD.setVisible(true);
        } else if (CHOOSE_OUTPUTFILE.equals(cmd)) {
            JFileChooser jf = new JFileChooser();
            if (!outfileF.getText().trim().equals(""))
                jf.setCurrentDirectory(new File(outfileF.getText().trim()));
            else if (curPath != null)
                jf.setCurrentDirectory(curPath);
            jf.setDialogTitle("Please select an output file");
            if (out_splitoutB.isSelected())
                jf.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            else
                jf.setFileSelectionMode(JFileChooser.FILES_ONLY);
            int retval = jf.showSaveDialog(getMainFrame());
            if (retval == JFileChooser.APPROVE_OPTION) {
                File tf = jf.getSelectedFile();
                if (tf != null) {
                    outfile = new File(jf.getSelectedFile().getAbsolutePath());
                    if (verbose > 2)
                        System.err.println("[Gui] Selected output file: "
                                + outfile.toString());
                }
                curPath = jf.getCurrentDirectory();
                outfileF.setText(outfile.getAbsolutePath());
            }
        } else if (CHOOSE_OUTFORMATOPTS.equals(cmd)) {
            outfD.setVisible(true);
        } else if (CHOOSE_GRAMMARDIR.equals(cmd)) {
            JFileChooser jf = new JFileChooser();
            if (!grammarF.getText().trim().equals(""))
                jf.setCurrentDirectory(new File(outfileF.getText().trim()));
            else if (curPath != null)
                jf.setCurrentDirectory(curPath);
            jf.setDialogTitle("Please select an output location");
            jf.setFileSelectionMode(JFileChooser.FILES_AND_DIRECTORIES);
            int retval = jf.showSaveDialog(getMainFrame());
            if (retval == JFileChooser.APPROVE_OPTION) {
                File tf = jf.getSelectedFile();
                if (tf != null) {
                    grammarfile = new File(jf.getSelectedFile()
                            .getAbsolutePath());
                    if (verbose > 2)
                        System.err.println("[Gui] Selected output file: "
                                + grammarfile.toString());
                }
                curPath = jf.getCurrentDirectory();
                grammarF.setText(grammarfile.getAbsolutePath());
            }
        } else if (TOGGLE_SHELL.equals(cmd)) {
            if (getShellFrame().isVisible())
                getShellFrame().setVisible(false);
            else
                getShellFrame().setVisible(true);
        } else if (CLEAR_SHELL.equals(cmd)) {
            getShell().setText("");
        } else if (SET_VERBOSE.equals(cmd)) {
            String s = (String) JOptionPane.showInputDialog(getMainFrame(),
                    "Enter verbose level:\n", "Verbose level",
                    JOptionPane.PLAIN_MESSAGE, null, null, "");
            try {
                verbose = Integer.valueOf(s);
                if (verbose > 0)
                    System.err.println("Verbose level set to " + verbose);
            } catch (NumberFormatException ex) {
            }
        } else if (QUIT.equals(cmd)) {
            System.exit(0);
        } else if (ABOUT.equals(cmd)) {
            about();
        }
    }

}
