package sDecorator;

/* File Name: client
 * Author: @bGZo
 * Created Time: 3/23/2022 18:46
 * License: MIT
 * Description:
 */
public class client {
    public static void main(String args[]){
        person xc = new person("Ming");

        System.out.println("Decorate:");

        tShorts ts = new tShorts();
        sneakers ss = new sneakers();
        trouser tr = new trouser();

        ts.decorate(xc);
        ss.decorate(ts);
        tr.decorate(ss);

        tr.show();
    }
}
