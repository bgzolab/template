package ch01_1;

import edu.princeton.cs.algs4.StdOut;

/* File Name: ex07
 * Author: @bGZo
 * Created Time: 4/4/2022 11:52
 * License: MIT
 * Description:
 */

public class ex07 {
    public static void a(double t){
        double tmp=t;
        while(Math.abs(t - tmp/t) > .000000001){
            t = (tmp/t + t)/2.0;
        }
        StdOut.printf("%.5f\n", t);
    } // sqrt(t)


    public static void main(String[] args){
        int sum = 0;
        for(int i=0; i<1000; i++){
            for(int j=0; j<i; j++){
                sum++;
            }
        }
        StdOut.println(sum);
    }
}
