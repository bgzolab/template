package vStrategy;

public class v3CashClient {
    static double total = 0.0d;
    public static void main(String[] args){
//        v3CashSuper csuper = v3CashFactory.createCashAccept(cbxType.Selection.ToString()); //DemoClient
        double totalPrice = 0d;
//        totalPrice = csuper.acceptCash(price *num); //DemoClient
        total += totalPrice;
        System.out.println( totalPrice );
    }
}
