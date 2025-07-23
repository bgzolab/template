package vInterpreter;

/* File Name: Move
 * Author: bGZo
 * Created Time: 6/24/2022 16:21
 * License: MIT
 * Description:终极表达式
 */
public class Move implements Expression{
    private int x, y;

    public Move(int x, int y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public void interpret() {
        System.out.println("移动鼠标：【" + x + "," + y + "】");
    }
}
