package vInterpreter;

/* File Name: LeftKeyUp
 * Author: bGZo
 * Created Time: 6/24/2022 16:22
 * License: MIT
 * Description:终极表达式
 */
public class LeftKeyUp implements Expression{
    @Override
    public void interpret() {
        System.out.println("松开鼠标：左键");
    }
}
