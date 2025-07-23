package vState;

/* File Name: Switcher
 * Author: bGZo
 * Created Time: 6/24/2022 13:15
 * License: MIT
 * Description:
 * + 开关状态校验
 */
public class Switcher {
    private boolean state = false;

    public void switchOn(){
        if(state == false){
            state = true;
            System.out.println("OK...使灯亮");
        }else{
            System.out.println("ERROR!!!开启状态下无须再开启");
        }
    }

    public void switchOff(){
        if(state == true){
            state = false;
            System.out.println("OK...使灯灭");
        }else{
            System.out.println("ERROR!!!关闭状态下无须再关闭");
        }
    }
}
