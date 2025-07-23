package vInterpreter;

/* File Name: Repetition
 * Author: bGZo
 * Created Time: 6/24/2022 16:26
 * License: MIT
 * Description:
 */
public class Repetition implements Expression{
    private int loopCount;
    private Expression loopBodySequence; // 循环体内的子表达式序列

    public Repetition(Expression loopBodySequence, int loopCount) {
        this.loopBodySequence = loopBodySequence;
        this.loopCount = loopCount;
    }

    @Override
    public void interpret() {
        // 此处并不关心 loopBodySequence 中还包含哪些子表达式，只迭代
        while (loopCount > 0) {
            loopBodySequence.interpret();
            loopCount--;
        }
    }
}
