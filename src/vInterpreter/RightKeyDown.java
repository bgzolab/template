package vInterpreter;

/* File Name: RightKeyDown
 * Author: bGZo
 * Created Time: 6/24/2022 16:30
 * License: MIT
 * Description:
 */
public class RightKeyDown implements Expression{
    @Override
    public void interpret() {
        System.out.println("按下鼠标：右键");
    }
}
