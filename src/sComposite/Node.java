package sComposite;

/* File Name: Node
 * Author: bGZo
 * Created Time: 6/23/2022 13:23
 * License: MIT
 * Description:
 */
public abstract class Node {
    protected String name;

    public Node(String name){
        this.name = name;
    }

    protected abstract void add(Node child);

    protected void tree(int space){

        for(int i=0; i<space; i++)
            System.out.print("  "); //├───

        System.out.println(name);
    }

    protected void tree(){
        this.tree(0);
    }

}
