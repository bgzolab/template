package vVisitor;

import java.time.LocalDate;

/* File Name: Candy
 * Author: bGZo
 * Created Time: 6/24/2022 14:54
 * License: MIT
 * Description:
 */
public class Candy extends Product implements Acceptable{
    public Candy(String name, LocalDate producedDate, float price) {
        super(name, producedDate, price);
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
