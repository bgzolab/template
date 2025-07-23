package cc.bgzo.x3exception;

/* File Name: x31ImplementWithException
 * Author: bGZo
 * Created Time: 11/6/2022 17:35
 * License: MIT
 * Description:
 */
public class x31ImplementWithException implements x31InterfaceWithException{
    /**
     * NOTE:
        * 接口中是否声明异常, 抛和不抛都是可以的;
            * 声明异常只可以抛出 声明的类或其子类
            * 未声明的只可以抛出 Runtime Exception;
                * 想要抛 Checked Exception 也得 Catch 后封装在 Runtime Exception 中, 否者报错;
     */
    @Override
    public void safe() { }

    @Override
    public void danger()
//            throws Exception
    {}
}
