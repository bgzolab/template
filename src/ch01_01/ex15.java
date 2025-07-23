package ch01_1;

import java.util.Scanner;

/* File Name: ex15
 * Author: @bGZo
 * Created Time: 4/17/2022 20:35
 * License: MIT
 * Description:
 */
public class ex15 {
    public static int[] histogram(int[] a, int M){
        int[] result = new int[M];
        for (int i = 0; i < a.length; i++) {
            if (a[i] >= 0 && a[i] < M) {
                result[a[i]]++;
            }
        }
        return result;

    }

    public static void main(String[] args) {
        int[] a = { 1, 1, 2, 3, 1, 7, 5, 3, 2, 2, 2 };
        int[] result = histogram(a, 8);
        for (int i = 0; i < result.length; i++) {
            System.out.printf("%3d", result[i]);
        }
    }
}
