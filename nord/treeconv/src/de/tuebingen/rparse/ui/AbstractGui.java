package de.tuebingen.rparse.ui;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import javax.swing.JComponent;
import javax.swing.JDialog;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JRootPane;
import javax.swing.JTextArea;
import javax.swing.KeyStroke;

public abstract class AbstractGui {

    private JFrame mainFrame = null;
    private JFrame shellFrame = null;
    private JTextArea shell = null;

    private PrintStream errs = new PrintStream(new StderrStream(this, new ByteArrayOutputStream()));

    public AbstractGui(String title) {
        System.setErr(errs);
        shell = new JTextArea();
        mainFrame = new JFrame(title);
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        shellFrame = new JFrame(title + " shell");
    }

    public JFrame getMainFrame() {
        return mainFrame;
    }

    public void setMainFrame(JFrame mainFrame) {
        this.mainFrame = mainFrame;
    }

    public JFrame getShellFrame() {
        return shellFrame;
    }

    public void setShellFrame(JFrame shellFrame) {
        this.shellFrame = shellFrame;
    }

    public void setShell(JTextArea shell) {
        this.shell = shell;
    }

    public JTextArea getShell() {
        return shell;
    }

    public void showError(String msg) {
        JOptionPane.showMessageDialog(mainFrame, msg, "Error",
                JOptionPane.ERROR_MESSAGE);
    }

    public void showMessage(String msg) {
        JOptionPane.showMessageDialog(mainFrame, msg, "Information",
                JOptionPane.INFORMATION_MESSAGE);
    }

    public class GuiDialog extends JDialog implements ActionListener {

        public void actionPerformed(ActionEvent e) {
            this.setVisible(false);
        }

        protected JRootPane createRootPane() {
            KeyStroke stroke1 = KeyStroke.getKeyStroke(KeyEvent.VK_ESCAPE, 0);
            KeyStroke stroke2 = KeyStroke.getKeyStroke(KeyEvent.VK_ENTER, 0);
            JRootPane rootPane = new JRootPane();
            rootPane.registerKeyboardAction(this, stroke1,
                    JComponent.WHEN_IN_FOCUSED_WINDOW);
            rootPane.registerKeyboardAction(this, stroke2,
                    JComponent.WHEN_IN_FOCUSED_WINDOW);
            return rootPane;
        }

        private static final long serialVersionUID = 1L;
    }

}
