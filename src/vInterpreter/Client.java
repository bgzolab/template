package vInterpreter;

import java.util.Arrays;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 16:29
 * License: MIT
 * Description:
 */
public class Client {
    /*
     * BEGIN            // 脚本开始
     * MOVE 500,600;    // 鼠标指针移动到坐标(500, 600)
     *   BEGIN LOOP 5   // 开始循环5次
     *      LEFT_CLICK; // 循环体内单击左键
     *      DELAY 1;    // 每次延迟1秒
     *   END;           // 循环体结束
     * RIGHT_DOWN;      // 按下右键
     * DELAY 7200;      // 延迟2小时
     * END;             // 脚本结束
     */
    public static void main(String[] args) {
        // 构造指令集语义树，实际情况会交给语法分析器（Evaluator or Parser）
        Expression sequence = new Sequence( Arrays.asList(
                new Move(500, 600),
                new Repetition(
                        new Sequence(
                                Arrays.asList(new LeftKeyClick(), new Delay(1))),
                        5 // 循环5次
                ),
                new RightKeyDown(),
                new Delay(7200)
        ));

        sequence.interpret();
    }
}
