package vState;

/* File Name: TrafficLight
 * Author: bGZo
 * Created Time: 6/24/2022 13:22
 * License: MIT
 * Description:
 */
public class TrafficLight {
    State state = new Red();

    public void setState(State state) {
        this.state = state;
    }

    public void switchToGreen() {
        state.switchToGreen(this);
    }

    public void switchToYellow() {
        state.switchToYellow(this);
    }

    public void switchToRed() {
        state.switchToRed(this);
    }
}
