package cc.bgzo.x3exception;
import java.io.IOException;

/* File Name: x60Finally
 * Author: bGZo
 * Created Time: 11/6/2022 20:26
 * License: MIT
 * Description:
 */
public class x60Finally {
    public static void main(String[] args) {
        catchMultiNew();
        catchMultiOld();
        catchMultiTypeMultiMatch();
    }

    private static void catchMultiOld() {
        try {
            /**
             * NOTE: 如果一个方法抛出多种异常，可以针对多个类型有多种catch语语句
             */
            throwMultiException(0);
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static void catchMultiTypeMultiMatch() {
        try {
            /**
             * NOTE: catch的类型不能有多种匹配可能，否则会出错
             */
            throwMultiException(0);
//            throwMultiException(1);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void catchMultiNew() {
        try {
            throwMultiException(0);
        } catch (ClassNotFoundException | IOException e) {
            /**
             * NOTE: 如果捕获了不同类型的异常，但是处理方式一样，可以用简化模式
             */
            e.printStackTrace();
        }
    }

    private static void throwMultiException(int i) throws ClassNotFoundException, IOException {
        switch (i) {
            case 1:
                throw new NullPointerException("demo");
            case 2:
                throw new ClassNotFoundException("demo");
            case 3:
                throw new IOException("demo");
        }
    }
}
