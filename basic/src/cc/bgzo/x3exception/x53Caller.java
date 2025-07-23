package cc.bgzo.x3exception;

/* File Name: x53Caller
 * Author: bGZo
 * Created Time: 11/6/2022 18:59
 * License: MIT
 * Description:
 */
public class x53Caller {
    x54Caller x54caller = new x54Caller();

    public void call2Exception() throws x50MyException {
        System.out.println("Caller1.call2Exception开始");
        x54caller.call3Exception();
        System.out.println("Caller1.call2Exception结束");
    }

    /**
     * NOTE: 不用 throws ClassNotFoundException, 因为已经 Catch 了;
     */
    public void call2RTException() {
        System.out.println("Caller1.call2RTException开始");
        x54caller.call3RTException();
        System.out.println("Caller1.call2RTException结束");
    }

}

