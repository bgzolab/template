package cc.bgzo.x3exception;

/* File Name: x53Caller
 * Author: bGZo
 * Created Time: 11/6/2022 18:59
 * License: MIT
 * Description:
 */
public class x41Caller {
    x42Caller x42caller = new x42Caller();

    public void call2Exception() {
        System.out.println("Caller1.call2Exception开始");
        try {
            x42caller.call3Exception();
        } catch (ClassNotFoundException ex) {
            System.out.println("got exception in Caller1: "+ex.getMessage());
        }
        System.out.println("Caller1.call2Exception结束");
    }

    /**
     * NOTE: 不用 throws ClassNotFoundException, 因为已经 Catch 了;
     */
    public void call2RTException() {
        System.out.println("Caller1.call2RTException开始");
        x42caller.call3RTException();
        System.out.println("Caller1.call2RTException结束");
    }

}

