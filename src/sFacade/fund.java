package sFacade;

/* File Name: fund
 * Author: @bGZo
 * Created Time: 3/25/2022 10:30
 * License: MIT
 * Description:
 */
public class fund {
    stock1 gu1;
    stock2 gu2;
    nationalDebt1 nd1;
    realty1 rt1;

    public fund(){
        gu1 = new stock1();
        gu2 = new stock2();
        nd1 = new nationalDebt1();
        rt1 = new realty1();
    }

    public void buyFund(){
        gu1.buy();
        gu2.buy();
        nd1.buy();
        rt1.buy();
    }

    public void sellFund(){
        gu1.sell();
        gu2.sell();
        nd1.sell();
        rt1.sell();
    }

}
