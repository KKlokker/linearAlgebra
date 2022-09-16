public class matrixOperations {
    public static void main(String[] args) {
        fraction[][] matrix1 = intToFracMatrix(new int[][] {
            {1,0,-1},
            {1,-2,1},
            {2,0,1}
        });
        fraction[][] matrix2 = intToFracMatrix(new int[][] {
            {0,0,-2,0,7,12},
            {2,4,-10,6,12,28},
            {2,4,-5,6,-5,-1}
        });

        fraction[][] identity = identity(3,3);
        fraction[][] copy = copy(matrix1);
        eliminate(copy, 0, identity);
        System.out.println("------Double echeleon--------");
        printMatrixDouble(copy);
        System.out.println("-------Inverse-------");
        printMatrixDouble(identity);
        System.out.println("------original--------");
        printMatrixDouble(matrix1);
        System.out.println("------submatrix--------");
        printMatrix(submatrix(matrix1,1,1));
        System.out.println("------Determinant--------");
        System.out.println(determinant(matrix1));
        System.out.println("------Multiple--------");
        printMatrix(multiply(matrix1,identity));
    }

    public static void add(fraction[][] matrix1, fraction[][] matrix2) {
        for(int row = 0; row < matrix1.length; row++)
            for(int column = 0; column < matrix1[row].length; column++)
                matrix1[row][column].add(matrix2[row][column]);
    }

    public static void subtract(fraction[][] matrix1, fraction[][] matrix2) {
        for(int row = 0; row < matrix1.length; row++)
            for(int column = 0; column < matrix1[row].length; column++)
                matrix1[row][column].subtract(matrix2[row][column],new fraction(1));
    }

    public static fraction[][] multiply(fraction[][] matrix1, fraction[][] matrix2) {
        fraction[][] sum = emptyMatrix(matrix1.length,matrix2[0].length);
        for(int row = 0; row < matrix1.length; row++)
            for(int column = 0; column < matrix1[row].length; column++)
                for(int counter = 0; counter < matrix2[row].length; counter++) 
                    sum[row][counter].add(matrix1[row][column],matrix2[column][counter]);
        return sum;
    }

    public static double trace(fraction[][] matrix) {
        double sum = 0;
        for(int i = 0; i < matrix.length; i++)
            sum += matrix[i][i].value();
        return sum;
    }

    public static void scalar(fraction[][] matrix, int scalar) {
        for(int row = 0; row < matrix.length; row++)
            for(int column = 0; column < matrix[0].length; column++)
                matrix[row][column].multiply(new fraction(scalar));
    }

    public static void transpose(fraction[][] matrix) {
        fraction[][] transposed = new fraction[matrix[0].length][matrix.length];
        for(int row = 0; row < matrix.length; row++)
            for(int column = 0; column < matrix[0].length; column++)
                transposed[column][row] = matrix[row][column];
    }

    public static fraction[][] intToFracMatrix(int[][] matrix) {
        fraction[][] fracs = new fraction[matrix.length][matrix[0].length];
        for(int row = 0; row < matrix.length; row++)
            for(int column = 0; column < matrix[0].length; column++)
                fracs[row][column] = new fraction(matrix[row][column]);
        return fracs;
    }

    public static void eliminate(fraction[][] matrix, int beginningRow, fraction[][] inverse) {
        if(matrix.length == beginningRow) {
            beginningRow--;
            int lastLeadingOne = -1;
            for(int row = beginningRow; row >= 0 && lastLeadingOne == -1; row--)
                for(int column = 0; column < matrix[row].length && lastLeadingOne == -1; column++)
                    if(matrix[row][column].isOne()) lastLeadingOne = row;
            reduce(matrix, lastLeadingOne, inverse);
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
        swap(inverse, leftMostRow, beginningRow);
        //Divide row with left most column value
        i = 0;
        fraction division = matrix[beginningRow][leftMostColumn].inverted().copy();
        while(i < matrix[leftMostRow].length) {
            inverse[beginningRow][i].multiply(division);
            matrix[beginningRow][i].multiply(division);
            i++;
        }
        //subtract needed multiples to bottom rows
        for(int row = beginningRow+1; row < matrix.length; row++) {
            fraction times = matrix[row][leftMostColumn].copy();
            if(!times.isZero())
                for(int column = 0; column < matrix[row].length; column++) {
                    matrix[row][column].subtract(matrix[beginningRow][column], times);
                    inverse[row][column].subtract(inverse[beginningRow][column], times);
                }
        }
        eliminate(matrix, beginningRow+1, inverse);
    }

    public static void reduce(fraction[][] matrix, int beginningRow, fraction[][] inverse) {
        if(beginningRow < 0) return;
        int leadingOneColumn = 0;
        while(leadingOneColumn < matrix[beginningRow].length && matrix[beginningRow][leadingOneColumn].isZero()) leadingOneColumn++;
        //subtract needed multiples to top rows
            for(int row = beginningRow-1; row >= 0; row--) {
                fraction times = matrix[row][leadingOneColumn].copy();
                if(!times.isZero())
                    for(int column = 0; column < matrix[row].length; column++) {
                        matrix[row][column].subtract(matrix[beginningRow][column], times);
                        inverse[row][column].subtract(inverse[beginningRow][column], times);
                    }
            }
        reduce(matrix,beginningRow-1, inverse);
    }

    public static fraction determinant(fraction[][] matrix) {
        if(matrix.length == 1 && matrix[0].length == 1) return matrix[0][0];
        fraction sum = new fraction(0);
        for(int i = 0; i < matrix.length; i++) {
            fraction elem = new fraction((int) Math.pow(isEven(i, 0), 1+0));
            elem.multiply(matrix[i][0]);
            elem.multiply(determinant(submatrix(matrix,i,0)));
            sum.add(elem);
        }
        return sum;
    }

    private static fraction[][] submatrix(fraction[][] matrix, int row, int column) {
        fraction[][] submatrix = new fraction[matrix.length-1][matrix[0].length-1];
        for(int i = 0; i < matrix.length; i++) 
            if(i != row) 
                for(int j = 0; j < matrix[0].length; j++)
                    if(j != column) {
                        int columnPlacement = j > column ? j -1 : j;
                        int rowPlacement = i > row ? i -1 : i;
                        submatrix[rowPlacement][columnPlacement] = matrix[i][j];
                    }
        return submatrix;
    }

    private static int isEven(int i, int j) {
        return 1-((i+j)%2)*2;
    }

    public static void swap(fraction[][] matrix, int row1, int row2) {
        fraction[] tempRow = matrix[row1];
        matrix[row1] = matrix[row2];
        matrix[row2] = tempRow; 
    }

    public static fraction[][] identity(int rows, int columns) {
        fraction[][] identity = emptyMatrix(rows, columns);
        int smallest = rows > columns ? columns : rows;
        for(int i = 0; i < smallest; i++)
            identity[i][i] = new fraction(1);
        return identity;
    }

    public static fraction[][] emptyMatrix(int rows, int columns) {
        fraction[][] emptyMatrix = new fraction[rows][columns];
        for(int i = 0; i < rows; i++)
            for(int j = 0; j < columns; j++)
                emptyMatrix[i][j] = new fraction(0);
        return emptyMatrix;
    }

    public static fraction[][] copy(fraction[][] matrix) {
        fraction[][] copy = new fraction[matrix.length][matrix[0].length];
        for(int row = 0; row < matrix.length; row++)
            for(int column = 0; column < matrix[0].length; column++)
                copy[row][column] = matrix[row][column].copy();
        return copy;
    }

    public static void printMatrix(fraction[][] matrix) {
        for(int row = 0; row < matrix.length; row++){
            System.out.print('|');
            for(int column = 0; column < matrix[row].length; column++)
                System.out.print(matrix[row][column] + ", ");
            System.out.println('|');
        }
    }

    public static void printMatrixDouble(fraction[][] matrix) {
        for(int row = 0; row < matrix.length; row++){
            System.out.print('|');
            for(int column = 0; column < matrix[row].length; column++) {
                if(matrix[row][column].value() >= 0) System.out.print('+');
                System.out.print(Math.round(matrix[row][column].value()*100)/100);
                if(column != matrix[row].length -1)
                    System.out.print(", ");
            }
            System.out.println('|');
        }
    }
}
