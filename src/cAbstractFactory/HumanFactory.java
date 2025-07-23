package cAbstractFactory;

/* File Name: HumanFactory
 * Author: bGZo
 * Created Time: 6/22/2022 00:00
 * License: MIT
 * Description:
 */
public class HumanFactory implements AbstractFactory{
    private int x;
    private int y;

    public HumanFactory(int x, int y){
        this.x = x;
        this.y = y;
    }

    @Override
    public LowClassUnit createLowClass() {
        LowClassUnit unit = new Marine(x, y);
        System.out.println("制造海军陆战队员成功。");
        return unit;
    }

    @Override
    public MidClassUnit createMidClass() {
        MidClassUnit unit = new Tank(x, y);
        System.out.println("制造变形坦克成功。");
        return unit;
    }

    @Override
    public HighClassUnit createHighClass() {
        HighClassUnit unit = new Battleship(x, y);
        System.out.println("制造巨型战舰成功。");
        return unit;
    }
}
