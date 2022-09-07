import java.io.Console;

public class gaussian {
    public static void main(String[] args) {
        fraction[][] matrix = new fraction[][]{
            {new fraction(1), new fraction(3),new fraction(-2),new fraction(0),new fraction(2),new fraction(0),new fraction(0)},
            {new fraction(2), new fraction(6),new fraction(-5),new fraction(-2),new fraction(4),new fraction(-3),new fraction(-1)},
            {new fraction(0), new fraction(0),new fraction(5),new fraction(10),new fraction(0),new fraction(15),new fraction(5)},
            {new fraction(2), new fraction(6),new fraction(0),new fraction(8),new fraction(4),new fraction(18),new fraction(6)}
        };
        eliminate(matrix, 0);
        printMatrix(matrix);
        
    }

    public static void eliminate(fraction[][] matrix, int beginningRow) {
        if(matrix.length == beginningRow) {
            beginningRow--;
            int lastLeadingOne = -1;
            for(int row = beginningRow; row >= 0 && lastLeadingOne == -1; row--)
                for(int column = 0; column < matrix[row].length && lastLeadingOne == -1; column++)
                    if(matrix[row][column].isOne()) lastLeadingOne = row;
            reduce(matrix, lastLeadingOne);
            return;
        }
        //Locate left most column not existing of zeroes
        int leftMostRow = beginningRow;
        int leftMostColumn= 0;
        boolean found = false;
        int i = 0; //column
        while(i < matrix[0].length && !found) {
            int j = beginningRow;
            while(j < matrix.length && matrix[j][i].isZero()) j++;
            if(j != matrix.length) {found = true; leftMostRow = j; leftMostColumn = i;}
            i++;
        }
        i--;
        swap(matrix, beginningRow, leftMostRow);
        //Divide row with left most column value
        i = leftMostColumn;
        fraction division = matrix[beginningRow][leftMostColumn].inverted();
        while(i < matrix[leftMostRow].length) {matrix[beginningRow][i].multiply(division);i++;}
        //subtract needed multiples to bottom rows
        for(int row = beginningRow+1; row < matrix.length; row++) {
            fraction times = matrix[row][leftMostColumn].copy();
            if(!times.isZero())
                for(int column = 0; column < matrix[row].length; column++) {
                    matrix[row][column].subtract(matrix[beginningRow][column], times);
                }
        }
        eliminate(matrix, beginningRow+1);
    }

    public static void reduce(fraction[][] matrix, int beginningRow) {
        if(beginningRow < 0) return;
        int leadingOneColumn = 0;
        while(leadingOneColumn < matrix[beginningRow].length && matrix[beginningRow][leadingOneColumn].isZero()) leadingOneColumn++;
        
        //subtract needed multiples to top rows
        if(leadingOneColumn < matrix[beginningRow].length-1)
            for(int row = beginningRow-1; row >= 0; row--) {
                fraction times = matrix[row][leadingOneColumn].copy();
                if(!times.isZero())
                    for(int column = 0; column < matrix[row].length; column++) {
                        matrix[row][column].subtract(matrix[beginningRow][column], times);
                    }
            }
        reduce(matrix,beginningRow-1);
    }

    public static void swap(fraction[][] matrix, int row1, int row2) {
        fraction[] tempRow = matrix[row1];
        matrix[row1] = matrix[row2];
        matrix[row2] = tempRow; 
    }

    public static void printMatrix(fraction[][] matrix) {
        for(int row = 0; row < matrix.length; row++){
            System.out.print('|');
            for(int column = 0; column < matrix[row].length; column++)
                System.out.print(matrix[row][column] + ", ");
            System.out.println('|');
        }
    }

}