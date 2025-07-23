package vChainOfResponsibility;

/* File Name: Manager
 * Author: bGZo
 * Created Time: 6/24/2022 13:38
 * License: MIT
 * Description:
 */
public class Manager extends Approver{
    public Manager(String name) {
        super(name);
    }

    @Override
    public void approve(int amount) {
        if (amount <= 5000) {
            System.out.println("审批通过。【经理：" + name + "】");
        } else {
            System.out.println("无权审批，请找上级。【经理：" + name + "】");
            this.nextApprover.approve(amount);
        }
    }
}
