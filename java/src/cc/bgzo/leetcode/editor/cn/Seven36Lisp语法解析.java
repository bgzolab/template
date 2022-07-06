package cc.bgzo.leetcode.editor.cn;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.HashMap;
import java.util.Map;

public class Seven36Lisp语法解析 {
    public static void main(String[] args) {
        Solution solution = new Seven36Lisp语法解析().new Solution();
    }

    //leetcode submit region begin(Prohibit modification and deletion)
    class Solution {
        Map<String, Deque<Integer>> scope = new HashMap<String, Deque<Integer>>();

        public int evaluate(String expression) {
            Deque<Deque<String>> vars = new ArrayDeque<Deque<String>>();
            int start = 0, n = expression.length();
            Deque<Expr> stack = new ArrayDeque<Expr>();
            Expr cur = new Expr(ExprStatus.VALUE);
            while (start < n) {
                if (expression.charAt(start) == ' ') {
                    start++; // 去掉空格
                    continue;
                }
                if (expression.charAt(start) == '(') {
                    start++; // 去掉左括号
                    stack.push(cur);
                    cur = new Expr(ExprStatus.NONE);
                    continue;
                }
                StringBuffer sb = new StringBuffer();
                if (expression.charAt(start) == ')') { // 本质上是把表达式转成一个 token
                    start++; // 去掉右括号
                    if (cur.status == ExprStatus.LET2) {
                        sb = new StringBuffer(Integer.toString(cur.value));
                        for (String var : vars.peek()) { // 清除作用域
                            scope.get(var).pop();
                        }
                        vars.pop();
                    } else if (cur.status == ExprStatus.ADD2) {
                        sb = new StringBuffer(Integer.toString(cur.e1 + cur.e2));
                    } else {
                        sb = new StringBuffer(Integer.toString(cur.e1 * cur.e2));
                    }
                    cur = stack.pop(); // 获取上层状态
                } else {
                    while (start < n && expression.charAt(start) != ' ' && expression.charAt(start) != ')') {
                        sb.append(expression.charAt(start));
                        start++;
                    }
                }
                String token = sb.toString();
                switch (cur.status.toString()) {
                    case "VALUE":
                        cur.value = Integer.parseInt(token);
                        cur.status = ExprStatus.DONE;
                        break;
                    case "NONE":
                        if ("let".equals(token)) {
                            cur.status = ExprStatus.LET;
                            vars.push(new ArrayDeque<String>()); // 记录该层作用域的所有变量, 方便后续的清除
                        } else if ("add".equals(token)) {
                            cur.status = ExprStatus.ADD;
                        } else if ("mult".equals(token)) {
                            cur.status = ExprStatus.MULT;
                        }
                        break;
                    case "LET":
                        if (expression.charAt(start) == ')') { // let 表达式的最后一个 expr 表达式
                            cur.value = calculateToken(token);
                            cur.status = ExprStatus.LET2;
                        } else {
                            cur.var = token;
                            vars.peek().push(token); // 记录该层作用域的所有变量, 方便后续的清除
                            cur.status = ExprStatus.LET1;
                        }
                        break;
                    case "LET1":
                        scope.putIfAbsent(cur.var, new ArrayDeque<Integer>());
                        scope.get(cur.var).push(calculateToken(token));
                        cur.status = ExprStatus.LET;
                        break;
                    case "ADD":
                        cur.e1 = calculateToken(token);
                        cur.status = ExprStatus.ADD1;
                        break;
                    case "ADD1":
                        cur.e2 = calculateToken(token);
                        cur.status = ExprStatus.ADD2;
                        break;
                    case "MULT":
                        cur.e1 = calculateToken(token);
                        cur.status = ExprStatus.MULT1;
                        break;
                    case "MULT1":
                        cur.e2 = calculateToken(token);
                        cur.status = ExprStatus.MULT2;
                        break;
                }
            }
            return cur.value;
        }

        public int calculateToken(String token) {
            if (Character.isLowerCase(token.charAt(0))) {
                return scope.get(token).peek();
            } else {
                return Integer.parseInt(token);
            }
        }
    }

    enum ExprStatus {
        VALUE,     // 初始状态
        NONE,      // 表达式类型未知
        LET,       // let 表达式
        LET1,      // let 表达式已经解析了 vi 变量
        LET2,      // let 表达式已经解析了最后一个表达式 expr
        ADD,       // add 表达式
        ADD1,      // add 表达式已经解析了 e1 表达式
        ADD2,      // add 表达式已经解析了 e2 表达式
        MULT,      // mult 表达式
        MULT1,     // mult 表达式已经解析了 e1 表达式
        MULT2,     // mult 表达式已经解析了 e2 表达式
        DONE       // 解析完成
    }

    class Expr {
        ExprStatus status;
        String var; // let 的变量 vi
        int value; // VALUE 状态的数值，或者 LET2 状态最后一个表达式的数值
        int e1, e2; // add 或 mult 表达式的两个表达式 e1 和 e2 的数值

        public Expr(ExprStatus s) {
            status = s;
        }
    } // via: https://leetcode.cn/problems/parse-lisp-expression/solution/lisp-yu-fa-jie-xi-by-leetcode-solution-zycb/
//leetcode submit region end(Prohibit modification and deletion)

}
// Lisp 语法解析
//给你一个类似 Lisp 语句的字符串表达式 expression，求出其计算结果。 
//
// 表达式语法如下所示: 
//
// 
// 表达式可以为整数，let 表达式，add 表达式，mult 表达式，或赋值的变量。表达式的结果总是一个整数。 
// (整数可以是正整数、负整数、0) 
// let 表达式采用 "(let v1 e1 v2 e2 ... vn en expr)" 的形式，其中 let 总是以字符串 "let"来表示，接下来会跟
//随一对或多对交替的变量和表达式，也就是说，第一个变量 v1被分配为表达式 e1 的值，第二个变量 v2 被分配为表达式 e2 的值，依次类推；最终 let 表达
//式的值为 expr表达式的值。 
// add 表达式表示为 "(add e1 e2)" ，其中 add 总是以字符串 "add" 来表示，该表达式总是包含两个表达式 e1、e2 ，最终结果是 
//e1 表达式的值与 e2 表达式的值之 和 。 
// mult 表达式表示为 "(mult e1 e2)" ，其中 mult 总是以字符串 "mult" 表示，该表达式总是包含两个表达式 e1、e2，最终结果
//是 e1 表达式的值与 e2 表达式的值之 积 。 
// 在该题目中，变量名以小写字符开始，之后跟随 0 个或多个小写字符或数字。为了方便，"add" ，"let" ，"mult" 会被定义为 "关键字" ，不会
//用作变量名。 
// 最后，要说一下作用域的概念。计算变量名所对应的表达式时，在计算上下文中，首先检查最内层作用域（按括号计），然后按顺序依次检查外部作用域。测试用例中每一个表
//达式都是合法的。有关作用域的更多详细信息，请参阅示例。 
// 
// 
//
// 示例 1： 
//
// 
//输入：expression = "(let x 2 (mult x (let x 3 y 4 (add x y))))"
//输出：14
//解释：
//计算表达式 (add x y), 在检查变量 x 值时，
//在变量的上下文中由最内层作用域依次向外检查。
//首先找到 x = 3, 所以此处的 x 值是 3 。
// 
//
// 示例 2： 
//
// 
//输入：expression = "(let x 3 x 2 x)"
//输出：2
//解释：let 语句中的赋值运算按顺序处理即可。
// 
//
// 示例 3： 
//
// 
//输入：expression = "(let x 1 y 2 x (add x y) (add x y))"
//输出：5
//解释：
//第一个 (add x y) 计算结果是 3，并且将此值赋给了 x 。 
//第二个 (add x y) 计算结果是 3 + 2 = 5 。
// 
// 
//
// 提示： 
//
// 
// 1 <= expression.length <= 2000 
// exprssion 中不含前导和尾随空格 
// expressoin 中的不同部分（token）之间用单个空格进行分隔 
// 答案和所有中间计算结果都符合 32-bit 整数范围 
// 测试用例中的表达式均为合法的且最终结果为整数 
// 
// Related Topics 栈 递归 哈希表 字符串 👍 153 👎 0
