package vCommand.TVs;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/* File Name: Keyboard
 * Author: bGZo
 * Created Time: 6/24/2022 14:43
 * License: MIT
 * Description:
 */
public class Keyboard {
    public enum KeyCode {
        F1, F2, ESC, UP, DOWN, LEFT, RIGHT;
    }

    private Map<KeyCode, List<Command>> keyCommands = new HashMap<>();

    // 按键与命令映射
    public void bindKeyCommand(KeyCode keyCode, List<Command> commands) {
        this.keyCommands.put(keyCode, commands);
    }

    // 触发按键
    public void onKeyPressed(KeyCode keyCode) {
        System.out.println(keyCode + "键按下……");
        List<Command> commands = this.keyCommands.get(keyCode);
        if (commands == null) {
            System.out.println(" 警告：无效的命令。");
            return;
        }
        commands.stream().forEach(command -> command.exe());
    }
}
