package ch01_02;

import edu.princeton.cs.algs4.StdOut;

/* File Name: ex04
 * Author: @bGZo
 * Created Time: 4/18/2022 22:37
 * License: MIT
 * Description:
 */
public class ex05 {
    public static void main(String[] args){
        String s = "Hello World";
        s.toUpperCase();
        s.substring(6,11);
        String str = s.substring(6,11);
        StdOut.println(s);
        StdOut.println(str);
    }
}
/* ex04
    String str1 = "hello";
        String str2 = str1;
        str1 = "world";
        StdOut.println(str1);
        StdOut.println(str2);
* */
