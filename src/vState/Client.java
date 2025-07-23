package vState;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 13:27
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        TrafficLight trafficLight = new TrafficLight();
        trafficLight.switchToYellow();
        trafficLight.switchToGreen();
        trafficLight.switchToYellow();
        trafficLight.switchToRed();
        trafficLight.switchToGreen(); // Error Msg
    }
}
