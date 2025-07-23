package vInterpreter;

/* File Name: LeftKeyDown
 * Author: bGZo
 * Created Time: 6/24/2022 16:21
 * License: MIT
 * Description:终极表达式
 */
public class LeftKeyDown implements Expression{
    @Override
    public void interpret() {
        System.out.println("按下鼠标：左键");
    }
}
