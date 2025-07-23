package vCommand.TVs;

/* File Name: TVChannelUpCommand
 * Author: bGZo
 * Created Time: 6/24/2022 14:42
 * License: MIT
 * Description:
 */
public class TVChannelUpCommand implements Command{

    private TV tv;

    public TVChannelUpCommand(TV tv) {
        this.tv = tv;
    }

    @Override
    public void exe() {
        tv.channelUp();
    }

    @Override
    public void unexe() {
        tv.channelDown();
    }

}
