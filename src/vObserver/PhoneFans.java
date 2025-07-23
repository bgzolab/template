package vObserver;

/* File Name: PhoneFans
 * Author: bGZo
 * Created Time: 6/24/2022 16:09
 * License: MIT
 * Description:
 */
public class PhoneFans extends Buyer{

    public PhoneFans(String name) {
        super(name);
    }

    @Override
    public void inform(String product) {
        if(product.contains("手机")){//此买家只购买手机
            System.out.print(name);
            System.out.println("购买：" + product);
        }
    }
}
