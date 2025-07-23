package cc.bgzo.x3exception;

/* File Name: x55Caller
 * Author: bGZo
 * Created Time: 11/6/2022 19:00
 * License: MIT
 * Description:
 */
public class x55Caller {
    public void callThrowException() throws x50MyException {
        System.out.println("Caller3.callThrowException开始");
        String className = "not.existed.class";
        try {
            Class.forName(className);
        } catch (ClassNotFoundException e) {
            throw new x50MyException("尝试加载类出错：" + className, e);
        }
        System.out.println("Caller3.callThrowException结束");
    }

    public void callThrowRTException() {
        System.out.println("Caller3.callThrowRTException开始");
        try {
            Object n = null;
            n.toString();
        } catch (NullPointerException e){
            throw new x51MyRTException("执行toString的时候出错了", e);
        }
        System.out.println("Caller3.callThrowRTException结束");
    }
}