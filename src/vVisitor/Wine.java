package vVisitor;

import java.time.LocalDate;

/* File Name: Wine
 * Author: bGZo
 * Created Time: 6/24/2022 14:55
 * License: MIT
 * Description:
 */
public class Wine extends Product implements Acceptable{
    public Wine(String name, LocalDate producedDate, float price) {
        super(name, producedDate, price);
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
