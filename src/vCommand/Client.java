package vCommand;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 14:32
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) throws InterruptedException {
        Switcher switcher = new Switcher();             // 命令请求方
        Bulb bulb = new Bulb();                         // 命令执行方
        Command flashCommand = new FlashCommand(bulb);  // 闪烁命令


        switcher.setCommand(flashCommand);
        switcher.buttonPush();
        Thread.sleep(3000);                         // NOTE: Exception
        switcher.buttonPop();
    }
}
