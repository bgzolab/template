package vCommand;

/* File Name: Switcher
 * Author: bGZo
 * Created Time: 6/24/2022 14:03
 * License: MIT
 * Description:
 */
public class Switcher {

    private Command command;
//    private Bulb bulb;

    public void setCommand(Command command){
        this.command = command;
    }

    public void buttonPush() {      // 按钮触发事件
        System.out.println("按下按钮……");
        command.exe();
    }

    public void buttonPop() {
        System.out.println("弹起按钮……");
        command.unexe();
    }

}
