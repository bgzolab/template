package vStrategy;

/* File Name: v3CashRebate
 * Author: @bGZo
 * Created Time: 3/22/2022 23:52
 * License: MIT
 * Description:
 */

class v3CashRebate extends v3CashSuper{
    private  double moneyRebate = 1d;

    public v3CashRebate(String moneyRebate){
        this.moneyRebate = Double.parseDouble(moneyRebate);
    }

    @Override
    public  double acceptCash(double money) {
        return money * moneyRebate;
    }
}
