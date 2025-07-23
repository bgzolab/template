package vObserver;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 16:12
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        Buyer tangSir = new PhoneFans("手机粉");
        Buyer barJee = new HandChopper("剁手族");
        Shop shop = new Shop();

        //预订注册
        shop.register(tangSir);
        shop.register(barJee);

        //商品到货
        shop.setProduct("猪肉炖粉条");
        shop.setProduct("橘子手机");
    }
}
