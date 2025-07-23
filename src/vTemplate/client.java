package vTemplate;

/* File Name: client
 * Author: @bGZo
 * Created Time: 3/25/2022 09:38
 * License: MIT
 * Description:
 */
public class client {
    public static void main(String []args){
        System.out.println("paper 1:");
        testPaper stuA = new testPaperA();
        stuA.testQ1();
        stuA.testQ2();
        stuA.testQ3();

        testPaper stuB = new testPaperB();
        stuB.testQ1();
        stuB.testQ2();
        stuB.testQ3();
    }
}
