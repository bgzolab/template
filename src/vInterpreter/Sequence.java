package vInterpreter;

import java.util.List;

/* File Name: Sequence
 * Author: bGZo
 * Created Time: 6/24/2022 16:28
 * License: MIT
 * Description:
 */
public class Sequence implements Expression{
    private List<Expression> expressions; // 表达式列表

    public Sequence(List<Expression> expressions) {
        this.expressions = expressions;
    }

    public void interpret() {
        expressions.forEach(exp -> exp.interpret());
    }
}
