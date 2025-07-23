package ch01_1;

import java.util.Scanner;

/* File Name: ex14
 * Author: @bGZo
 * Created Time: 4/17/2022 20:28
 * License: MIT
 * Description:
 */
public class ex14 {

    public static int lg(int N){
        int step=-1;
        int sum=1;
        while(sum <= N){
            sum *= 2;
//            sum >>= 1;
            step++;
        }
        return step;
    }

    public static void main(String[] args) {
        Scanner i = new Scanner(System.in);
        int tmp = i.nextInt();
        System.out.println(lg(tmp));
    }
}