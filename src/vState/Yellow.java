package vState;

/* File Name: Yellow
 * Author: bGZo
 * Created Time: 6/24/2022 13:24
 * License: MIT
 * Description:
 */
public class Yellow implements State{

    @Override
    public void switchToGreen(TrafficLight trafficLight) {
        trafficLight.setState(new Green());
        System.out.println("OK...绿灯亮起60秒");
    }

    @Override
    public void switchToYellow(TrafficLight trafficLight) {
        System.out.println("ERROR!!!已是黄灯状态无须再切换");
    }

    @Override
    public void switchToRed(TrafficLight trafficLight) {
        trafficLight.setState(new Red());
        System.out.println("OK...红灯亮起60秒");
    }
}
