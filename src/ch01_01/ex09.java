package ch01_1;

import edu.princeton.cs.algs4.StdOut;

/* File Name: ex09
 * Author: @bGZo
 * Created Time: 4/4/2022 12:34
 * License: MIT
 * Description:
 */
public class ex09 {
    public static String convertStr(int N){
        String s = "";
        for (int n=N;n>0;n/=2){
            s = (n%2) + s;
        }
        return s;
    }
    public static void main(String[] args) {
        StdOut.println(convertStr(0));
    }
}