package cc.bgzo.x3exception;

/* File Name: x30ThrowException
 * Author: bGZo
 * Created Time: 11/6/2022 15:55
 * License: MIT
 * Description:
 */
public class x30ThrowException {

    public void thorwIt() throws ClassNotFoundException, NoSuchFieldException {
        /**
         * NOTE: alt+enter, 扔出去给下一级处理;
         */
        Class clazz = Class.forName("abc");
        clazz.getField("");
    }

    public void newAndThrow(int status)
            throws Exception
            , RuntimeException
    /**
     * NOTE: Unchecked Exception 可以选择 抛出/不抛出;
     */
    {
        switch (status){
            case 1: throw new Exception();
                /**
                 * NOTE: Checked Exception 必须抛出
                 */
            case 0: throw new RuntimeException();
        }
    }

    public static void main(String[] args) {
        x30ThrowException x30throwException = new x30ThrowException();

        try {
            x30throwException.thorwIt();
        } catch (NoSuchFieldException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        try {
            x30throwException.newAndThrow(0);
            x30throwException.newAndThrow(1);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

}
