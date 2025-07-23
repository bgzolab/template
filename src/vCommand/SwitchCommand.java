package vCommand;

/* File Name: SwitchCommand
 * Author: bGZo
 * Created Time: 6/24/2022 14:24
 * License: MIT
 * Description:
 * 由于场景比较简单，我们将所有命令简化为一个类来实现了。
 * 其实更确切的做法是将每个命令封装为一个类，也就是可以
 * 进一步将其拆分为“开命令” (OnCommand) 与“关命令” (OffCommand)
 * 两个实现类，其中前者的执行方法中触发灯泡的开灯操作，
 * 反向执行方法中则触发灯泡的关灯操作，而后者则反之，
 * 以此支持更多高级功能
 */
public class SwitchCommand implements Command{
    private Bulb bulb;

    public SwitchCommand(Bulb bulb) {
        this.bulb = bulb;
    }

    @Override
    public void exe() {
        bulb.on();// 执行开灯操作
    }

    @Override
    public void unexe() {
        bulb.off();// 执行关灯操作
    }
}
