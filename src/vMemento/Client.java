package vMemento;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 19:19
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        Editor editor = new Editor(new Doc("《AI的觉醒》"));

        editor.append("第一章 混沌初开");
        editor.append("\n  正文2000字……");
        editor.append("\n第二章 荒漠之花\n  正文3000字……");
        editor.delete(); // 惨剧在此发生
        editor.undo();
    }
}
