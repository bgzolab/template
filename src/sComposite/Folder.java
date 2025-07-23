package sComposite;

import java.util.ArrayList;
import java.util.List;

/* File Name: Folder
 * Author: bGZo
 * Created Time: 6/23/2022 13:24
 * License: MIT
 * Description:
 */
public class Folder extends Node{

    private List<Node> childNodes = new ArrayList<>();

    public Folder(String name){
        super(name);
    }

    @Override
    protected void add(Node child) {
        childNodes.add(child);
    }

    @Override
    public void tree(int space){
        super.tree(space);

        space++;

        for(Node node: childNodes){
            node.tree(space);
        }
    }
}
