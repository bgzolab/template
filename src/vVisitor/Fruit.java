package vVisitor;

import java.time.LocalDate;

/* File Name: Fruit
 * Author: bGZo
 * Created Time: 6/24/2022 14:55
 * License: MIT
 * Description:
 */
public class Fruit extends Product implements Acceptable{

    private float weight;

    public Fruit(String name, LocalDate producedDate, float price, float weight) {
        super(name, producedDate, price);
        this.weight = weight;
    }

    public float getWeight(){
        return weight;
    }

    public void setWeight(float weight){
        this.weight = weight;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
