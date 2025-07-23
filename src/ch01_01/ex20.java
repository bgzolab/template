package ch01_1;

/* File Name: ex20
 * Author: @bGZo
 * Created Time: 4/17/2022 21:44
 * License: MIT
 * Description:
 */
public class ex20 {
    public static double ln(int N) {
        if (N == 0) {
            return 0;
        } else {
            return Math.log(N) + ln(N - 1);
        }
    }

    public static void main(String[] args) {
        System.out.println(ln(10));
    }
}
