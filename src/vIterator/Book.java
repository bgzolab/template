package vIterator;

import java.util.ArrayList;
import java.util.List;

/* File Name: Book
 * Author: bGZo
 * Created Time: 6/23/2022 16:16
 * License: MIT
 * Description: Archived
 */
public class Book {
    class Page {
        private int index;

        public Page(int index){
            this.index = index;
        }

        @Override
        public String toString(){
            return "阅读第" + this.index + "页";
        }
    }

    private List pages = new ArrayList<>();

    public Book(int pageSize) {
        for (int i = 0; i < pageSize; i++) {
            pages.add(new Page(i+1));
        }
    }

    public void read(){
        for (Object page: pages) /* NOTE: NOT Page?*/
            System.out.println(page);
    }
}
