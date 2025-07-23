package vChainOfResponsibility;

/* File Name: CFO
 * Author: bGZo
 * Created Time: 6/24/2022 13:39
 * License: MIT
 * Description:
 */
public class CFO extends Approver{

    public CFO(String name) {
        super(name);
    }

    public void approve(int amount) {
        if (amount <= 10000) {
            System.out.println("审批通过。【总监：" + name + "】");
        } else {
            System.out.println("驳回申请。【总监：" + name + "】");
        }
    }
}
