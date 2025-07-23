package cc.bgzo.x3exception;

/* File Name: x54Caller
 * Author: bGZo
 * Created Time: 11/6/2022 19:00
 * License: MIT
 * Description:
 */
public class x54Caller {
    x55Caller x55caller = new x55Caller();

    public void call3Exception() throws x50MyException {
        System.out.println("Caller2.call3Exception开始");
        x55caller.callThrowException();
        System.out.println("Caller2.call3Exception结束");
    }

    public void call3RTException() {
        System.out.println("Caller2.call3RTException开始");
        x55caller.callThrowRTException();
        System.out.println("Caller2.Caller2call3RTException结束");
    }
}
