package sProxy.Woo.Grils;

/* File Name: proxy
 * Author: @bGZo
 * Created Time: 3/23/2022 21:06
 * License: MIT
 * Description:
 */
public class proxy implements iGiveGift{
    pursuit gg;

    public proxy(schoolGirl mm){
        gg = new pursuit(mm); //???
    }

    @Override
    public void giveDoll() {
        gg.giveDoll();
    }

    @Override
    public void giveFlower() {
        gg.giveFlower();
    }

    @Override
    public void giveChocolate() {
        gg.giveChocolate();
    }
}
