package vChainOfResponsibility;

/* File Name: Approver
 * Author: bGZo
 * Created Time: 6/24/2022 13:53
 * License: MIT
 * Description:
 */
public abstract class Approver {

    protected String name;
    protected Approver nextApprover;            // 下一位审批人，更高级别领导

    public Approver(String name) {
        this.name = name;
    }

    protected Approver setNextApprover(Approver nextApprover) {
        this.nextApprover = nextApprover;
        return this.nextApprover;               // 返回下一位审批人，使其支持链式编程
    }

    public abstract void approve(int amount);   // 抽象审批方法由具体审批人子类实现

}
