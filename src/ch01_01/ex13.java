package ch01_1;

/* File Name: ex13
 * Author: @bGZo
 * Created Time: 4/17/2022 20:21
 * License: MIT
 * Description:
 */
public class ex13 {
    public static void printTranposeMartix(int [][]ma){
        for(int i=0;i<ma[0].length;i++){
            for(int j=0; j<ma.length;j++){
                System.out.print( ma[j][i] + " ");
            }
            System.out.println();
        }

    }

    public static void main(String[] args){
        int[][] a = { { 100, 200, 300 }, { 400, 500, 600 } };
        printTranposeMartix(a);
    }
}
