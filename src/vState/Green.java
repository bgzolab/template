package vState;

/* File Name: Green
 * Author: bGZo
 * Created Time: 6/24/2022 13:24
 * License: MIT
 * Description:
 */
public class Green implements State{

    @Override
    public void switchToGreen(TrafficLight trafficLight) {
        System.out.println("ERROR!!!已是绿灯状态无须再切换");
    }

    @Override
    public void switchToYellow(TrafficLight trafficLight) {
        trafficLight.setState(new Yellow());
        System.out.println("OK...黄灯亮起5秒");
    }

    @Override
    public void switchToRed(TrafficLight trafficLight) {
        System.out.println("ERROR!!!绿灯不能切换为红灯");
    }

}
