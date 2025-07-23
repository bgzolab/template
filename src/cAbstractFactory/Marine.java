package cAbstractFactory;

/* File Name: Marine
 * Author: bGZo
 * Created Time: 6/21/2022 22:49
 * License: MIT
 * Description:
 */
public class Marine extends LowClassUnit{

    public Marine(int x, int y){
        super(x, y);
    }

    @Override
    public void show() {
        System.out.println("士兵出现在坐标：[" + x + "," + y + "]");

    }

    @Override
    public void attack() {
        System.out.println("士兵用机关枪射击，攻击力：" + attack);
    }
}
