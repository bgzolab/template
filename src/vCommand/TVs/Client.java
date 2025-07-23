package vCommand.TVs;

import java.util.Arrays;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 14:44
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        Keyboard keyboard = new Keyboard();
        TV tv = new TV();
        Command tvOnCommand = new TVOnCommand(tv);
        Command tvOffCommand = new TVOffCommand(tv);
        Command tvChannelUpCommand = new TVChannelUpCommand(tv);

        //按键与命令映射
        keyboard.bindKeyCommand(
                Keyboard.KeyCode.F1,
                Arrays.asList(tvOnCommand)
        );
        keyboard.bindKeyCommand(
                Keyboard.KeyCode.LEFT,
                Arrays.asList(tvChannelUpCommand)
        );
        keyboard.bindKeyCommand(
                Keyboard.KeyCode.ESC,
                Arrays.asList(tvOffCommand)
        );

        //触发按键
        keyboard.onKeyPressed(Keyboard.KeyCode.F1);
        keyboard.onKeyPressed(Keyboard.KeyCode.LEFT);
        keyboard.onKeyPressed(Keyboard.KeyCode.UP);
        keyboard.onKeyPressed(Keyboard.KeyCode.ESC);
    }
}
