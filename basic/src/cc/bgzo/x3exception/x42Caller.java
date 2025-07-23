package cc.bgzo.x3exception;

/* File Name: x54Caller
 * Author: bGZo
 * Created Time: 11/6/2022 19:00
 * License: MIT
 * Description:
 */
public class x42Caller {
    x43Caller x43caller = new x43Caller();

    public void call3Exception() throws ClassNotFoundException {
        System.out.println("Caller2.call3Exception开始");
        x43caller.callThrowException();
        System.out.println("Caller2.call3Exception结束");
    }

    public void call3RTException() {
        System.out.println("Caller2.call3RTException开始");
        x43caller.callThrowRTException();
        System.out.println("Caller2.Caller2call3RTException结束");
    }
}
