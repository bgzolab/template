package vIterator;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 18:28
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        DrivingRecorder dr = new DrivingRecorder();


        for (int i = 0; i < 12; i++) {
            dr.append("视频_" + i);
        }

        //用户的U盘，用于复制交通事故视频
        List uStorage = new ArrayList<>();

        //获取迭代器
        Iterator it = dr.iterator();

        while (it.hasNext()) {//如果还有下一条则继续迭代
            String video = (String) it.next();
            System.out.println(video);
            //用户翻看视频发现第10条和第8条可作为证据
            if("视频_10".equals(video) || "视频_8".equals(video)){
                uStorage.add(video);
            }
        }

        System.out.println("事故证据：" + uStorage);

    }
}
