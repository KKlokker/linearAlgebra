public class fraction {
    private int numerator, denominator;
    
    public fraction(int numerator, int denominator) {
        this.numerator = numerator;
        this.denominator = denominator;
    }

    public fraction(int numerator) {
        this.numerator = numerator;
        this.denominator = 1;
    }

    public void subtract(fraction frac, fraction times) {
        fraction fracCopy = frac.copy();
        fracCopy.multiply(times);
        denominator = denominator * fracCopy.denominator;
        numerator = numerator * fracCopy.denominator - fracCopy.numerator;
        reduce();
    }

    public void multiply(fraction frac) {
        numerator = frac.numerator * numerator;
        denominator = frac.denominator * denominator;
        reduce();
    }

    public fraction copy() {
        return new fraction(numerator,denominator);
    }

    public boolean isZero() {
        return (numerator == 0 || denominator == 0);
    }

    public boolean isOne() {
        return (numerator == denominator);
    }

    public fraction inverted() {
        return new fraction(denominator, numerator);
    }

    private void reduce() {
        int d = gcd(numerator,denominator);
        if(d == 0) return;
        denominator = denominator / d;
        numerator = numerator / d;
    }

    private int gcd(int a, int b) {
        if(b == 0) return a;
        return gcd(b, a%b);
    }

    @Override public String toString() {
        return (Integer.toString(numerator) + '/' + Integer.toString(denominator));
    }
}
