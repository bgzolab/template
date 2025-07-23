package vMediator;

import java.util.Objects;

/* File Name: User
 * Author: bGZo
 * Created Time: 6/23/2022 21:22
 * License: MIT
 * Description:
 */
public class User {
    private String name;
    private ChatRoom chatRoom;

    public User(String name) {
        this.name = name;
    }
    public String getName() {
        return this.name;
    }

    public void login(ChatRoom chatRoom) {
        this.chatRoom = chatRoom;                       // 注入聊天室
        this.chatRoom.register(this);             // 连接聊天室
    }
    protected void logout() {
        chatRoom.deregister(this);                // 注销聊天室
        this.chatRoom = null;                           // 置空聊天室
    }

    protected void talk(User to, String msg) {//用户发言
        if (Objects.isNull(chatRoom)) {
            System.out.println("【" + name + "的对话框】" + "您还没有登录");
            return;
        }
        chatRoom.sendMsg(this, to, msg);                  //给聊天室发送消息
        // chatRoom.sendMsg(this, msg);
    }

    public void listen(User from, User to, String msg) {        //聆听方法
        System.out.print("【" + this.getName() + "的对话框】");
        System.out.println(chatRoom.processMsg(from, to, msg)); // 聊天室消息加工
        // System.out.println(fromWhom.getName() + " 说： " + msg);
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return Objects.equals(name, user.name);
    }
}
