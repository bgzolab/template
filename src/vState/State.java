package vState;

/* File Name: State
 * Author: bGZo
 * Created Time: 6/24/2022 13:21
 * License: MIT
 * Description:
 */
public interface State {

    void switchToGreen(TrafficLight trafficLight);

    void switchToYellow(TrafficLight trafficLight);

    void switchToRed(TrafficLight trafficLight);
}
