package sFlyweight;

/* File Name: River
 * Author: bGZo
 * Created Time: 6/23/2022 15:34
 * License: MIT
 * Description:
 */
public class River implements Drawable{
    private String image;

    public River() {
        this.image = "河流";
        System.out.print("从磁盘加载[" + image + "]图片，耗时半秒……");
    }

    @Override
    public void draw(int x, int y) {
        System.out.println("在位置[" + x + ":" + y + "]上绘制图片：[" + image + "]");
    }
}
