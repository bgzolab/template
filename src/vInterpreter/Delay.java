package vInterpreter;

/* File Name: Delay
 * Author: bGZo
 * Created Time: 6/24/2022 16:22
 * License: MIT
 * Description: 终极表达式
 */
public class Delay implements Expression{
    private int seconds;

    public Delay(int seconds) {
        this.seconds = seconds;
    }
    public int getSeconds() {
        return seconds;
    }

    public void interpret() {
        System.out.println("系统延迟：" + seconds + "秒");
        try {
            Thread.sleep(seconds * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
