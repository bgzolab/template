package sBridge;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 15:53
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        //白色画笔对应的所有形状
        new WhitePen(new CircleRuler()).draw();
        new WhitePen(new SquareRuler()).draw();
        new WhitePen(new TriangleRuler()).draw();

        //黑色画笔对应的所有形状
        new BlackPen(new CircleRuler()).draw();
        new BlackPen(new SquareRuler()).draw();
        new BlackPen(new TriangleRuler()).draw();
    }
}
