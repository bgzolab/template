package cc.bgzo.x3exception;

/* File Name: x20Category
 * Author: bGZo
 * Created Time: 11/6/2022 12:38
 * License: MIT
 * Description:
 */
public class x20Category {
    void NotHaveToHandle(){
        String str = null;
        str.toLowerCase();
    }
    void MustHandle(){
        try{
            Class clazz = Class.forName("cc.bgzo.x3exception.x20Category");
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
