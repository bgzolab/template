package ch01_1;

/* File Name: ex17
 * Author: @bGZo
 * Created Time: 4/17/2022 21:09
 * License: MIT
 * Description:
 */
public class ex17 {
    public static String exR2(int n) {
        String s = exR2(n - 3) + n + exR2(n - 2) + n;
        if (n <= 0) {
            return "";
        }
        return s;
    }
    public static void main(String[] args) {
        System.out.println(exR2(3));
    }
    //这段代码中的基础情况永远不会被访问。调用exR2(3)会产生调用exR2(0)、exR2(-3)和exR2(-6)，循环往复直到发生StackOverflowError
}
