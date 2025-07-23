package ch01_02;

import edu.princeton.cs.algs4.StdIn;

/* File Name: ex06
 * Author: @bGZo
 * Created Time: 4/18/2022 22:44
 * License: MIT
 * Description: todo
 */
public class ex06 {
    public static void main(String[] args) {
        System.out.print("s: ");
        String s = StdIn.readLine();
        System.out.print("t: ");
        String t = StdIn.readLine();
        if (s.length() == t.length() && s.concat(s).indexOf(t) >= 0) {
            System.out.println(s + " is the circular rotation of " + t);
        } else {
            System.out.println(s + " is not the circular rotation of " + t);
        }
    }


}
