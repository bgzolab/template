package sFlyweight;

/* File Name: House
 * Author: bGZo
 * Created Time: 6/23/2022 15:38
 * License: MIT
 * Description:
 */

public class House implements Drawable {
    private String image;

    public House() {
        this.image = "房屋";
        System.out.print("从磁盘加载[" + image + "]图片，耗时半秒……");
    }

    @Override
    public void draw(int x, int y) {
        System.out.print("将图层切换到顶层……");//房屋盖在地板上，所以切换到顶层图层
        System.out.println("在位置[" + x + ":" + y + "]上绘制图片：[" + image + "]");
    }

}