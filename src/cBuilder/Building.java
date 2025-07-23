package cBuilder;

import java.util.ArrayList;
import java.util.List;

/* File Name: Building
 * Author: bGZo
 * Created Time: 6/21/2022 18:41
 * License: MIT
 * Description: via: 秒懂设计模式 -> https://weread.qq.com/web/reader/9b13257072562b5c9b1c8d6kc51323901dc51ce410c121b
 */
public class Building {
    private List<String> buildComponents = new ArrayList<>();

    public void setBasement(String basement){
        this.buildComponents.add(basement);
    }

    public void setWall(String wall){
        this.buildComponents.add(wall);
    }

    public void setRoof(String roof){
        this.buildComponents.add(roof);
    }

    @Override
    public String toString() {
        String buildStr = "";
        for(int i = buildComponents.size()-1; i>=0; i--){
            buildStr += buildComponents.get(i);
        }

        return buildStr;
    }
}


