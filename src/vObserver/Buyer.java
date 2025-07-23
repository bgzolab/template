package vObserver;

/* File Name: Buyer
 * Author: bGZo
 * Created Time: 6/24/2022 16:02
 * License: MIT
 * Description:
 */
public abstract class Buyer {

    protected String name;

    public Buyer(String name) {
        this.name = name;
    }
    public abstract void inform(String product);

//    private Shop shop;
//    public void buy() {
//        System.out.print(name + "购买：");
//        System.out.println(shop.getProduct());
//    }
}
