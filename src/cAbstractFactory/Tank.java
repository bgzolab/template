package cAbstractFactory;

/* File Name: Tank
 * Author: bGZo
 * Created Time: 6/21/2022 23:51
 * License: MIT
 * Description:
 */
public class Tank extends MidClassUnit{
    public Tank(int x, int y){
        super(x, y);
    }

    @Override
    public void show() {
        System.out.println("坦克出现在坐标：[" + x + "," + y + "]");
    }

    @Override
    public void attack() {
        System.out.println("坦克用炮轰击，攻击力：" + attack);
    }
}
