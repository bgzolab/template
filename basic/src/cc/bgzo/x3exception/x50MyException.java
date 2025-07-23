package cc.bgzo.x3exception;

/* File Name: x30TestMyException
 * Author: bGZo
 * Created Time: 11/6/2022 12:21
 * License: MIT
 * Description:
 */
class x50MyException extends Exception{

    x50MyException() {}

    public x50MyException(String message) {
        super(message);
    }

    public x50MyException(String message, Throwable cause) {
        super(message, cause);
    }

    public x50MyException(Throwable cause) {
        super(cause);
    }
}