package cc.bgzo.x3exception;

/* File Name: x52UsingMyExceptionClass
 * Author: bGZo
 * Created Time: 11/6/2022 19:58
 * License: MIT
 * Description:
 */
public class x52UsingMyExceptionClass {
    void a() throws x50MyException {
        System.out.println("Throws MyException from a()");
        throw new x50MyException();
    }

    void b() throws x50MyException {
        System.out.println("Throws MyException from b()");
        throw new x50MyException();
    }

    void usingMyExceptionClass(){
        x52UsingMyExceptionClass usingMyExceptionClass = new x52UsingMyExceptionClass();

        try{
            usingMyExceptionClass.a();
        } catch (x50MyException e) {
            e.printStackTrace();
        }

        try{
            usingMyExceptionClass.b();
        } catch (x50MyException e) {
            e.printStackTrace();
        }

    }
    public static void main(String[] args) {
        x53Caller x53caller = new x53Caller();

        System.out.println("Begin");


        try {
            x53caller.call2Exception();
        } catch (x50MyException e) {
            /**
             * NOTE: Not using exception to normal logic
             */
            System.out.println( e.toString() + " : 收到！");
        }

        try {
            x53caller.call2RTException();
        } catch (Exception e) {
            /**
             * NOTE: Not using exception to normal logic
             */
            System.out.println(e.toString() + " : 收到！");
        }
        System.out.println("End");
    }
}
