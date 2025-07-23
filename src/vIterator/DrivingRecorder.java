package vIterator;

import java.util.Iterator;

/* File Name: DrivingRecorder
 * Author: bGZo
 * Created Time: 6/23/2022 18:23
 * License: MIT
 * Description:
 */
public class DrivingRecorder {

    private int index = -1;                     // 当前记录位置
    private String[] records = new String[10];  // 假设只能记录10条视频

    public void append(String record) {
        if (index == 9) index = 0;              // 索引重置，从头覆盖
        else            index++;                //正常覆盖下一条

        records[index] = record;
    }

    // FIXME: @Override
    public Iterator<String> iterator(){
        return new Itr();
    }

    private class Itr implements Iterator<String> {
        int cursor = index;
        int loopCount = 0;

        @Override
        public boolean hasNext(){
            return loopCount < 10;
        }
        @Override
        public String next(){
            int i = cursor;
            if(cursor == 0) cursor = 9;
            else            cursor--;
            loopCount++;
            return records[i];
        }
    }
    /* @Deprecated
    public void display() {                     // 循环显示所有记录 (10)
        for (int i = 0; i < 10; i++)
            System.out.println(i + ": " + records[i]);
    }

    public void displayByOrder() {              // 从新到旧显示记录 (10), NOTE: AWE!!
        for (int i = index, loopCount = 0; loopCount < 10;
             i = ((i == 0) ? 9 : i - 1), loopCount++)
            System.out.println(records[i]);
    }
    */
}