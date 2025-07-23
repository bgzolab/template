package vCommand.TVs;

/* File Name: TVOffCommand
 * Author: bGZo
 * Created Time: 6/24/2022 14:42
 * License: MIT
 * Description:
 */
public class TVOffCommand implements Command{

    private TV tv;

    public TVOffCommand(TV tv) {
        this.tv = tv;
    }

    @Override
    public void exe() {
        tv.off();
    }

    @Override
    public void unexe() {
        tv.on();
    }

}
