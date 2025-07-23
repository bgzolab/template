package cAbstractFactory;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/22/2022 00:03
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        System.out.println("游戏开始……");
        System.out.println("双方挖矿攒钱……");

        //第一位玩家选择了人类族
        System.out.println("工人建造人类族工厂……");
        AbstractFactory factory = new HumanFactory(10, 10);

        Unit marine = factory.createLowClass();
        marine.show();

        Unit tank = factory.createMidClass();
        tank.show();

        Unit ship = factory.createHighClass();
        ship.show();

        //第二位玩家选择了外星怪兽族
        System.out.println("工蜂建造外星怪兽族工厂……");
        factory = new AlienFactory(200, 200);

        Unit roach = factory.createLowClass();
        roach.show();

        Unit poison = factory.createMidClass();
        poison.show();

        Unit mammoth = factory.createHighClass();
        mammoth.show();

        System.out.println("两族开始大混战……");
        marine.attack();
        roach.attack();
        poison.attack();
        tank.attack();
        mammoth.attack();
        ship.attack();
    }
}
