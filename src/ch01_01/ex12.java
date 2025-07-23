package ch01_1;

/* File Name: ex12
 * Author: @bGZo
 * Created Time: 4/17/2022 20:18
 * License: MIT
 * Description:
 */
public class ex12 {
    public static void main(String[] args) {
        int[] a = new int[10];
        for (int i = 0; i < 10; i++) {
            a[i] = 9 - i;
        }
        for (int i = 0; i < 10; i++) {
            a[i] = a[a[i]];
        }
        // I think the author should ask this
        for (int i = 0; i < 10; i++) {
            System.out.println(a[i]);
        }
    }
}
