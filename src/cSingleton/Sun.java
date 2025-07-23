package cSingleton;

/* File Name: Sun
 * Author: bGZo
 * Created Time: 6/21/2022 20:10
 * License: MIT
 * Description:
 */
public class Sun {
    /*
     * Eager initialization
     * private static final Sun sun = new Sun();
     * */
    private static Sun sun;

    private Sun(){

    }

    public static Sun getInstance(){
        /*
        * lazy initialization
        * */
        if(sun == null){
            synchronized(Sun.class){
                if(sun == null){
                    sun = new Sun();
                }
            }
        }
        return sun;
    }
}
