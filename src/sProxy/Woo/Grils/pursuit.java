package sProxy.Woo.Grils;

/* File Name: pursuit
 * Author: @bGZo
 * Created Time: 3/23/2022 20:59
 * License: MIT
 * Description:
 */
public class pursuit implements iGiveGift{
    schoolGirl mm;

    public pursuit(schoolGirl mm){
        this.mm = mm;
    }

    @Override
    public void giveDoll() {
        System.out.println("Give " + mm.getName() + " a doll");
    }

    @Override
    public void giveFlower() {
        System.out.println("Give " + mm.getName() + " a flower");

    }

    @Override
    public void giveChocolate() {
        System.out.println("Give " + mm.getName() + " a chocolate");

    }
}
/*
*
*     public void giveDoll(schoolGirl mm) {
        gg = new schoolGirl(mm);
    }
*/
