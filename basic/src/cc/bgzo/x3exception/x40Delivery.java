package cc.bgzo.x3exception;

/* File Name: x40Delivery
 * Author: bGZo
 * Created Time: 11/6/2022 18:54
 * License: MIT
 * Description:
 */

public class x40Delivery {
    static x41Caller x41caller ;

    static void call2Exception() {
        x41caller = new x41Caller();
        System.out.println("调用开始");
        x41caller.call2Exception();
        System.out.println("调用结束");
    }

    static void call2RTException() {
        x41caller = new x41Caller();
        System.out.println("调用开始");
        x41caller.call2RTException();
        System.out.println("调用结束");
    }

    public static void main(String[] args) {
        call2Exception();
        call2RTException();
    }



}
