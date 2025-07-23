package sFlyweight;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 15:30
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        //先实例化图件工厂
        TileFactory factory = new TileFactory();

        //随便绘制一列为例
        factory.getDrawable("河流").draw(10, 10);
        factory.getDrawable("河流").draw(10, 20);
        factory.getDrawable("道路").draw(10, 30);
        factory.getDrawable("草地").draw(10, 40);
        factory.getDrawable("草地").draw(10, 50);
        factory.getDrawable("草地").draw(10, 60);
        factory.getDrawable("草地").draw(10, 70);
        factory.getDrawable("草地").draw(10, 80);
        factory.getDrawable("道路").draw(10, 90);
        factory.getDrawable("道路").draw(10, 100);

        //绘制完地板后接着在顶层绘制房屋
        factory.getDrawable("房子").draw(10, 10);
        factory.getDrawable("房子").draw(10, 50);
    }
}
