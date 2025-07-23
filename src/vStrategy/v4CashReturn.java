package vStrategy;

/* File Name: v3CashReturn
 * Author: @bGZo
 * Created Time: 3/22/2022 23:52
 * License: MIT
 * Description:
 */
public class v4CashReturn implements v4CashSuper{
    private  double moneyCondition = 0.0d;
    private  double moneyReturn = 0.0d;

    public v4CashReturn(String moneyCondition, String moneyReturn){
        this.moneyCondition = Double.parseDouble(moneyCondition);
        this.moneyReturn = Double.parseDouble(moneyReturn);
    }

    @Override
    public  double acceptCash(double money){
        double result = money;
        if( money >= this.moneyCondition )
            result = money - Math.floor(money/moneyCondition) * moneyReturn;
        return result;
    }
}