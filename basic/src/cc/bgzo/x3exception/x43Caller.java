package cc.bgzo.x3exception;

/* File Name: x55Caller
 * Author: bGZo
 * Created Time: 11/6/2022 19:00
 * License: MIT
 * Description:
 */
public class x43Caller {
    public void callThrowException() throws ClassNotFoundException {
        System.out.println("Caller3.callThrowException开始");
        Class.forName("not.existed.class");
        System.out.println("Caller3.callThrowException结束");
    }

    public void callThrowRTException() {
        System.out.println("Caller3.callThrowRTException开始");
        Object n = null;
        n.toString();
        System.out.println("Caller3.callThrowRTException结束");
    }
}