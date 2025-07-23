package vObserver;

import java.util.ArrayList;
import java.util.List;

/* File Name: Shop
 * Author: bGZo
 * Created Time: 6/24/2022 16:01
 * License: MIT
 * Description:
 */
public class Shop {

    private String product;
    private List<Buyer> buyers;             // 预订清单

    public Shop() {
        this.product = "无商品";
        this.buyers = new ArrayList<>();
    }

    public void register(Buyer buyer) {     // 注册买家到预订清单中
        this.buyers.add(buyer);
    }

    public String getProduct() {
        return product;
    }

    public void setProduct(String product) {
        this.product = product;             // 到货了
        notifyBuyers();                     // 到货后通知买家
    }

    public void notifyBuyers() {            // 通知所有注册买家
        buyers.stream().forEach(b -> b.inform(this.getProduct()));
    }
}
