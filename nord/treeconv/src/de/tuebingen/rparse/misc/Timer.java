package de.tuebingen.rparse.misc;

public class Timer {

    private long starttime;

    public Timer() {
    }

    public void start() {
        starttime = System.nanoTime();
    }

    public void reset() {
        starttime = 0;
    }

    public String time() {
        long ptime = System.nanoTime() - starttime;
        return String.valueOf((ptime) / (Math.pow(10, 9))) + " sec.";
    }

}
