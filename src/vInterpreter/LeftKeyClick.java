package vInterpreter;

/* File Name: LeftKeyClick
 * Author: bGZo
 * Created Time: 6/24/2022 16:24
 * License: MIT
 * Description: “按下左键”及“松开左键”两个原子操作组合
 */
public class LeftKeyClick implements Expression{
    private Expression leftKeyDown;
    private Expression leftKeyUp;

    public LeftKeyClick() {
        this.leftKeyDown = new LeftKeyDown();
        this.leftKeyUp = new LeftKeyUp();
    }

    @Override
    public void interpret() {
        // 使解释工作延续到子表达式里去
        leftKeyDown.interpret();
        leftKeyUp.interpret();
    }
}
