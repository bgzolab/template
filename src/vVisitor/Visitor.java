package vVisitor;

/* File Name: Visitor
 * Author: bGZo
 * Created Time: 6/24/2022 14:57
 * License: MIT
 * Description:
 */
public interface Visitor {
    public void visit(Candy candy);     // 重载糖果

    public void visit(Wine wine);       // 重载酒类

    public void visit(Fruit fruit);     // 重载水果
}
