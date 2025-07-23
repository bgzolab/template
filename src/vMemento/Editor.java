package vMemento;

import java.util.ArrayList;
import java.util.List;

/* File Name: Editor
 * Author: bGZo
 * Created Time: 6/23/2022 18:59
 * License: MIT
 * Description:
 */
public class Editor {

    private Doc doc;                        // 文档引用
    private List historyRecords;            // 历史记录列表
    private int historyPosition = -1;       // 历史记录当前位置

    public Editor(Doc doc) {
        System.out.println("<<<打开文档" + doc.getTitle());
        this.doc = doc;                     // 载入文档
        historyRecords = new ArrayList<>(); // 初始化历史记录列表
        backup();                           // 载入文档后保存第一份历史记录
        show();
    }

    public void append(String txt) {
        System.out.println("<<<插入操作");
        doc.setBody(doc.getBody() + txt);
        backup();                           // 添加后保存一份历史记录
        show();
    }

    public void delete(){
        System.out.println("<<<删除操作");
        doc.setBody("");
        backup();                           // 删除后保存一份历史记录
        show();
    }

    public void save(){
        System.out.println("<<<存盘操作");
    }

    private void backup() {
        historyRecords.add(doc.createHistory());
        historyPosition++;
    }

    private void show(){                    // 显示当前文档内容
        System.out.println(doc.getBody());
        System.out.println("文档结束>>>\n");
    }

    public void undo() {                    // 撤销操作：如按下组合键Ctrl+Z，回到过去
        System.out.println(">>>撤销操作");
        if (historyPosition == 0) return;   // 到头了，不能再撤销了

        historyPosition--;                  // 历史记录位置回溯一次
        History history = (History) historyRecords.get(historyPosition); // NOTE: Cast???
        doc.restoreHistory(history);        // 取出历史记录并恢复至文档
        show();
    }

    public void redo(){// 重做操作
        //此处省略
    }
}
