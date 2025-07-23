package vInterpreter;

/* File Name: RightKeyUp
 * Author: bGZo
 * Created Time: 6/24/2022 16:31
 * License: MIT
 * Description:
 */
public class RightKeyUp implements Expression{
    @Override
    public void interpret() {
        System.out.println("松开鼠标：右键");

    }
}
