package vVisitor;

import java.time.LocalDate;
import java.util.Arrays;
import java.util.List;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 15:09
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        List products = Arrays.asList(
                new Candy("小兔奶糖", LocalDate.of(2018, 10, 1), 20.00f),
                new Wine("老猫白酒", LocalDate.of(2017, 1, 1), 1000.00f),
                new Fruit("草莓", LocalDate.of(2018, 12, 26), 10.00f, 2.5f)
        );

        Visitor discountVisitor = new DiscountVisitor(LocalDate.of(2019, 1, 1));

        // 迭代购物车中的商品
        for (Object product : products) {
            // [java.lang Object cannot be converted]: Acceptable
            ((Acceptable)product).accept(discountVisitor);
        }

    }
}
