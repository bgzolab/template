package sBridge;

/* File Name: BlackPen
 * Author: bGZo
 * Created Time: 6/23/2022 15:52
 * License: MIT
 * Description:
 */
public class BlackPen extends Pen{

    public BlackPen(Ruler ruler){
        super(ruler);
    }

    @Override
    public void draw() {
        System.out.print("黑");
        ruler.regularize();
    }
}
