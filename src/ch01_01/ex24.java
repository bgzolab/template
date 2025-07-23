package ch01_1;

/* File Name: ex24
 * Author: @bGZo
 * Created Time: 4/17/2022 22:12
 * License: MIT
 * Description:todo
 */
public class ex24 {
    public static int euclid(int p, int q) {
        System.out.println("p = " + p + ", q = " + q);
        if (p == 0 || q == 0) {
            return 1;
        }
        if (p < q) {
            int t = p;
            p = q;
            q = t;
        }
        if (p % q == 0) {
            return q;
        } else {
            return euclid(q, p % q);
        }
    }

    public static void main(String[] args) {
        System.out.println("result: " + euclid(105, 24));
        System.out.println("result: " + euclid(1111111, 1234567));
    }
}
