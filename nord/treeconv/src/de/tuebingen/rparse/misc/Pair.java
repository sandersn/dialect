package de.tuebingen.rparse.misc;

public class Pair<T1, T2> {

    private T1 l;
    private T2 r;

    public Pair(T1 l, T2 r) {
        this.l = l;
        this.r = r;
    }

    public T1 getL() {
        return l;
    }

    public void setL(T1 l) {
        this.l = l;
    }

    public T2 getR() {
        return r;
    }

    public void setR(T2 r) {
        this.r = r;
    }

    public int hashCode() {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((l == null) ? 0 : l.hashCode());
        result = prime * result + ((r == null) ? 0 : r.hashCode());
        return result;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (!(obj instanceof Pair))
            return false;
        Pair<?, ?> other = (Pair<?, ?>) obj;
        if (l == null) {
            if (other.l != null)
                return false;
        } else if (!l.equals(other.l))
            return false;
        if (r == null) {
            if (other.r != null)
                return false;
        } else if (!r.equals(other.r))
            return false;
        return true;
    }

}
