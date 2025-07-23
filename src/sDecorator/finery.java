package sDecorator;

/* File Name: finery
 * Author: @bGZo
 * Created Time: 3/23/2022 18:39
 * License: MIT
 * Description:
 */
public class finery extends person{

    protected person component;

    public void decorate(person component){
        this.component = component;
    }
    @Override
    public void show(){
        if (component != null){
            component.show();
        }
    }
}
