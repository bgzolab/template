package ch01_02;

import edu.princeton.cs.algs4.StdIn;

/* File Name: ex07
 * Author: @bGZo
 * Created Time: 4/19/2022 00:03
 * License: MIT
 * Description:
 */
public class ex07 {
    public static String mystery(String s) {
        int N = s.length();
        if (N <= 1) {
            return s;
        }
        String a = s.substring(0, N / 2);
        String b = s.substring(N / 2, N);
        return mystery(b) + mystery(a);
    }

    public static void main(String[] args) {
        System.out.println(mystery(StdIn.readLine()));
    }
}
