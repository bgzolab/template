package sDecorator;

/* File Name: person
 * Author: @bGZo
 * Created Time: 3/23/2022 18:37
 * License: MIT
 * Description:
 */
public class person {
    private String name;

    public person(){}
    public person(String name){ this.name=name; }

    public void show(){System.out.println("decorated by " + this.name);}

}
