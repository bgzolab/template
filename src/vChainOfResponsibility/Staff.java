package vChainOfResponsibility;

/* File Name: Staff
 * Author: bGZo
 * Created Time: 6/24/2022 13:38
 * License: MIT
 * Description:
 */
public class Staff extends Approver{

    public Staff(String name) {
        super(name);
    }

    @Override
    public void approve(int amount) {
        if (amount <= 1000) {
            System.out.println("审批通过。【专员：" + name + "】");
        } else {
            System.out.println("无权审批，请找上级。【专员：" + name + "】");
            this.nextApprover.approve(amount);
        }
    }

}
