package cc.bgzo.x3exception;

/* File Name: x61TryCatchFinally
 * Author: bGZo
 * Created Time: 11/6/2022 20:34
 * License: MIT
 * Description:
 */
public class x61TryCatchFinally {

    private static int VAL = 0;

    public static void main(String[] args) {
        System.out.println(withFinally());
        System.out.println(VAL);

        noCatch();
    }

    private static int withFinally() {
        int len = 0;
        try {
            String s = null;
            return s.length();
        } catch (Exception ex) {
            len = -1;
            System.out.println("执行catch里的return语句");
            return len;
        } finally {
            /**
             * NOTE:
                * 无论是因为 return/exception, finally 都会执行
                * finally语句 在 return语句 执行之后; return 返回之前;
             */

            System.out.println("执行finally语句");

            /**
             * NOTE: finally 里的 return 语句会覆盖之前的 return
             */
//            return -1111;

            /**
             * NOTE: finally 里无法给 return 的变量 赋值
             */
//            len = -2;

            VAL = 999;
            System.out.println("finally语句执行完毕");
        }
    }

    private static int noCatch(){
        try {
            String s = null;
            return s.length();
        } finally {
            /**
             * NOTE: 是否 Catch 都会执行 finally
             */
            System.out.println("执行finally语句");
        }
    }

}
