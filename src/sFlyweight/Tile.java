package sFlyweight;

/* File Name: Tile
 * Author: bGZo
 * Created Time: 6/23/2022 15:27
 * License: MIT
 * Description:
 */
public class Tile {
    private String image;   // 图块材质
    private int x, y;       // 图块坐标

    public Tile(String image, int x, int y) {
        this.image = image;
        System.out.print("从磁盘加载[" + image + "]图片，耗时半秒……");
        this.x = x;
        this.y = y;
    }

    public void draw() {
        System.out.println("在位置[" + x + ":" + y + "]上绘制图片：[" + image + "]");
    }
}
