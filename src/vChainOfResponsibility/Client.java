package vChainOfResponsibility;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 13:57
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        Approver flightJohn = new Staff("张飞");

        flightJohn.setNextApprover(new Manager("关羽"))
                .setNextApprover(new CFO("刘备"));        // 链式编程配置责任链

        flightJohn.approve(1000);
        flightJohn.approve(4000);
        flightJohn.approve(9000);
        flightJohn.approve(88000);

    }
}
