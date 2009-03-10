package de.tuebingen.rparse.ui;

import java.io.FilterOutputStream;
import java.io.IOException;
import java.io.OutputStream;

import de.tuebingen.rparse.ui.AbstractGui;

public class StderrStream extends FilterOutputStream {

    private final AbstractGui gui;

    public StderrStream(AbstractGui gui, OutputStream os) {
        super(os);
        this.gui = gui;
    }

    public void write(byte b[]) throws IOException {
        String s = new String(b);
        this.gui.getShell().append(s);
        String st = this.gui.getShell().getText();
        if (st.length() > 2) {
            int nli = st.lastIndexOf('\n');
            if (nli > 0 && st.substring(0, nli).lastIndexOf('\n') > -1)
                this.gui.getShell().setCaretPosition(nli + 1);
        }
    }

    public void write(byte b[], int off, int len) throws IOException {
        String s = new String(b, off, len);
        this.gui.getShell().append(s);
        String st = this.gui.getShell().getText();
        if (st.length() > 2) {
            int nli = st.lastIndexOf('\n');
            if (nli > 0 && st.substring(0, nli).lastIndexOf('\n') > -1)
                this.gui.getShell().setCaretPosition(nli + 1);
        }
    }
}
