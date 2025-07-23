package vStrategy;

/* File Name: v3CashFactory
 * Author: @bGZo
 * Created Time: 3/22/2022 23:58
 * License: MIT
 * Description:
 */

public class v3CashFactory {
    public static v3CashSuper createCashAccept(String type){
        v3CashSuper cs = null;

        switch (type){
            case "Normal":
                cs = new v3CashNormal();
                break;
            case "Return":
                v3CashReturn cr1 = new v3CashReturn("300","100");
                cs = cr1;
                break;
            case "Rebate":
                v3CashRebate cr2 = new v3CashRebate("0.8");
                cs = cr2;
                break;
        }
        return cs;
    }
}
