package vStrategy;

/* File Name: v4Context
 * Author: @bGZo
 * Created Time: 3/23/2022 00:26
 * License: MIT
 * Description:
 */
public class v4CashContext {
    private v4CashSuper cs=null; //Strategy strategy;

//    public v4CashContext(v4CashSuper csuper){
//        this.cs = csuper;
//    }

    public v4CashContext(String type) {
        switch (type){
            case "Normal":
                v4CashNormal cs0 = new v4CashNormal();
                cs=cs0;
                break;
            case "Return":
                v4CashReturn cr1 = new v4CashReturn("300","100");
                cs = cr1;
                break;
            case "Rebate":
                v4CashRebate cr2 = new v4CashRebate("0.8");
                cs = cr2;
                break;
        }
    }

    public double getResult(double money){ //contextInterface
        return  cs.acceptCash(money);
    }
}
