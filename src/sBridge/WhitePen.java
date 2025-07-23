package sBridge;

/* File Name: WhitePen
 * Author: bGZo
 * Created Time: 6/23/2022 15:59
 * License: MIT
 * Description:
 */
public class WhitePen extends Pen{
    public WhitePen(Ruler ruler) {
        super(ruler);
    }

    @Override
    public void draw() {
        System.out.print("白");
        ruler.regularize();
    }
}
