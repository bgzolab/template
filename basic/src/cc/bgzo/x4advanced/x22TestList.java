package cc.bgzo.x4advanced;

import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedList;
import java.util.List;

/* File Name: x22TestList
 * Author: bGZo
 * Created Time: 11/6/2022 22:20
 * License: MIT
 * Description:
 */
public class x22TestList {
    public static void main(String[] args) {
        printCollection(addElementsToCollection(new ArrayList()));
        printCollection(addElementsToCollection(new LinkedList()));

//        printCollection(addElementsToCollection(new x20ArrayList()));
//        printCollection(addElementsToCollection(new x20ArrayList()));

        printList((List) addElementsToCollection(new ArrayList()));
        printList((List) addElementsToCollection(new x20ArrayList()));
        printList((List) addElementsToCollection(new x21LinkedList()));
    }


    public static Collection addElementsToCollection(Collection collection) {
        for (int i = 0; i < 10; i++) {
            collection.add("str" + (i % 5));
        }
        return collection;
    }

    public static void printCollection(Collection collection) {
        System.out.println();
        System.out.println("输出" + collection.getClass() + "中的元素，共" + collection.size() + "个");
        try {
            for (Object element : collection) {
                System.out.println(element);
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public static void printList(List list) {
        System.out.println();
        System.out.println("输出" + list.getClass() + "中的元素，共" + list.size() + "个");
        for (int i = 0; i < list.size(); i++) {
            System.out.println(list.get(i));
        }
    }

}
