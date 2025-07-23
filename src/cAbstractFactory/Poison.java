package cAbstractFactory;

/* File Name: Poison
 * Author: bGZo
 * Created Time: 6/21/2022 23:57
 * License: MIT
 * Description:
 */
public class Poison extends MidClassUnit{
    Poison(int x,int y){
        super(x, y);
    }

    @Override
    public void show() {
        System.out.println("毒液兵出现在坐标：[" + x + "," + y + "]");
    }

    @Override
    public void attack() {
        System.out.println("毒液兵用毒液喷射，攻击力：" + attack);
    }
}
