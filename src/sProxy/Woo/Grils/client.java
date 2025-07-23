package sProxy.Woo.Grils;

/* File Name: client
 * Author: @bGZo
 * Created Time: 3/23/2022 21:09
 * License: MIT
 * Description:
 */
public class client {
    public static void main(String args[]){
        schoolGirl JingRong = new schoolGirl("JingRong");
        proxy thirdPerson = new proxy(JingRong);

        thirdPerson.giveDoll();
        thirdPerson.giveFlower();
        thirdPerson.giveChocolate();

    }
}
