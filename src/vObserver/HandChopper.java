package vObserver;

/* File Name: HandChopper
 * Author: bGZo
 * Created Time: 6/24/2022 16:11
 * License: MIT
 * Description:
 */
public class HandChopper extends Buyer{
    public HandChopper(String name) {
        super(name);
    }

    @Override
    public void inform(String product) {
        System.out.print(name);
        System.out.println("购买：" + product);
    }

}
