package ch01_1;

import edu.princeton.cs.algs4.StdIn;

/* File Name: ex18
 * Author: @bGZo
 * Created Time: 4/17/2022 21:12
 * License: MIT
 * Description:
 */
public class ex18 {
    public static int mystery(int a, int b) {
        if (b == 0) {
            return 0;
        }
        if (b % 2 == 0) return mystery(a + a, b / 2);
        else return mystery(a + a, b / 2) + a;
    }// it'd better,

    public static int mystery2(int a, int b) {
        if (b == 0) {
            return 1;
        }
        if (b % 2 == 0) return mystery2(a * a, b / 2);
        else return mystery2(a * a, b / 2) * a;
    }

    public static void main(String[] args) {
//        int a = StdIn.readInt();
//        int b = StdIn.readInt();

//        System.out.println(mystery(2, 25));
        System.out.println(mystery(3, 11));
    }
}
