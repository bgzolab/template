package vStrategy;

/* File Name: v3CashRebate
 * Author: @bGZo
 * Created Time: 3/22/2022 23:52
 * License: MIT
 * Description:
 */

class v4CashRebate implements v4CashSuper{
    private  double moneyRebate = 1d;

    public v4CashRebate(String moneyRebate){
        this.moneyRebate = Double.parseDouble(moneyRebate);
    }

    @Override
    public  double acceptCash(double money) {
        return money * moneyRebate;
    }
}
