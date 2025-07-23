package ch01_1;

/* File Name: ex16
 * Author: @bGZo
 * Created Time: 4/17/2022 21:00
 * License: MIT
 * Description:
 */
public class ex16 {

    public static String exR1(int n){
        if(n <= 0) return "";
        return exR1(n-3)+n+exR1(n-2)+n;
    }
    public static void main(String[] args) {
        System.out.println(exR1(6));
    /*
    * (3) 6 (4) 6
    * */
    }
}
