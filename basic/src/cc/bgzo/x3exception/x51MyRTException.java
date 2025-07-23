package cc.bgzo.x3exception;

/* File Name: x51MyRTException
 * Author: bGZo
 * Created Time: 11/6/2022 19:48
 * License: MIT
 * Description:
 */
public class x51MyRTException extends RuntimeException{

    public x51MyRTException() {}

    public x51MyRTException(String message) {
        super(message);
    }

    public x51MyRTException(String message, Throwable cause) {
        super(message, cause);
    }

    public x51MyRTException(Throwable cause) {
        super(cause);
    }
}
