package sBridge;

/* File Name: Pen
 * Author: bGZo
 * Created Time: 6/23/2022 15:51
 * License: MIT
 * Description:
 */
public abstract class Pen {

    protected Ruler ruler;

    public Pen(Ruler ruler){
        this.ruler = ruler;
    }

    public abstract void draw();

}
