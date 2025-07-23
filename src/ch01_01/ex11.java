package ch01_1;

/* File Name: ex11
 * Author: @bGZo
 * Created Time: 4/17/2022 19:35
 * License: MIT
 * Description:
 */
public class ex11 {
    public static void printMatrix(boolean[][] ma){
        for(int i=0;i<ma.length;i++){
            for(int j=0; j<ma[i].length;j++){
//                if( ma[i][j]==true ) System.out.print("*");
//                else System.out.print(" ");
                System.out.print( ma[i][j]? "*":" ");
            }
            System.out.println();
        }
    }

    public static void main(String[] args){
        boolean[][] a = { { true, false, true }, { false, true, false },
                { true, true, false } };
        printMatrix(a);
    }
}
