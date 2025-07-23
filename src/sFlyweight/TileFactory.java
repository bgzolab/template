package sFlyweight;

import java.util.HashMap;
import java.util.Map;

/* File Name: TileFactory
 * Author: bGZo
 * Created Time: 6/23/2022 15:38
 * License: MIT
 * Description:
 */
public class TileFactory {
    private Map<String, Drawable> images;

    public TileFactory(){
        images = new HashMap<String, Drawable>();
    }

    public Drawable getDrawable(String image){
        //缓存池里如果没有图件，则实例化并放入缓存池
        if(!images.containsKey(image)){
            switch (image) {
                case "河流":
                    images.put(image, new River());
                    break;
                case "草地":
                    images.put(image, new Grass());
                    break;
                case "道路":
                    images.put(image, new Road());
                    break;
                case "房子":
                    images.put(image, new House());
            } // FIXME: Null Pointer Exception!!!
        }

        //至此，缓存池里必然有图件，直接取得并返回
        return images.get(image);
    }
}
