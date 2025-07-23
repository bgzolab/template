package ch01_1;

import edu.princeton.cs.algs4.StdOut;

/* File Name: ex06
 * Author: @bGZo
 * Created Time: 4/4/2022 06:13
 * License: MIT
 * Description:
 */
public class ex06 {
    public static void main(String[] args){
        int f = 0;
        int g = 1;
        for (int i=0; i<=15; i++){
            StdOut.println(f);
            f = f + g;
            g = f - g;
        }
    } //斐波那契数列
}
