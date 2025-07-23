package vCommand.TVs;

/* File Name: TVOnCommand
 * Author: bGZo
 * Created Time: 6/24/2022 14:41
 * License: MIT
 * Description:
 */
public class TVOnCommand implements Command{

    private TV tv;

    public TVOnCommand(TV tv) {
        this.tv = tv;
    }

    @Override
    public void exe() {
        tv.on();
    }

    @Override
    public void unexe() {
        tv.off();
    }
}
