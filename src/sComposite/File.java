package sComposite;

/* File Name: File
 * Author: bGZo
 * Created Time: 6/23/2022 13:26
 * License: MIT
 * Description:
 */
public class File extends Node{

    public File(String name){
        super(name);
    }

    @Override
    protected void add(Node child) {
        System.out.println("不能添加子节点!");
    }

    @Override
    public void tree(int space){
        super.tree(space);
    }
}
