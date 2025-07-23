package cc.bgzo.x3exception;

/* File Name: x44CallStack
 * Author: bGZo
 * Created Time: 11/6/2022 19:37
 * License: MIT
 * Description:
 */
public class x44CallStack {
    public static void main(String[] args) {
        callStack(9);
    }

    private static void callStack(int i) {
        i--;
        if (i == 0) {
            return;
        } else {
            if (i % 2 == 0) {
                m0(i);
            } else {
                m1(i);
            }
        }
    }

    private static void m1(int i) {
        System.out.println("m1\t" + i + "开始");
        callStack(i);
        System.out.println("m1\t" + i + "结束");
    }

    private static void m0(int i) {
        System.out.println("m0\t" + i + "开始");
        callStack(i);
        System.out.println("m0\t" + i + "结束");
    }
}
