package cBuilder;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/21/2022 19:01
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {

        Director director = new Director(new HouseBuilder());
        System.out.println(director.direct());

        director.setBuilder(new ApartmentBuilder());
        System.out.println(director.direct());

    }
}
