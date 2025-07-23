package vMediator;

import java.util.ArrayList;
import java.util.List;

/* File Name: ChatRoom
 * Author: bGZo
 * Created Time: 6/24/2022 10:04
 * License: MIT
 * Description:
 */
public abstract class ChatRoom {

    protected String name;
    List<User> users = new ArrayList<>();

    public ChatRoom(String name) {
        this.name = name;
    }

    public void register(User user) {
        this.users.add(user);
        System.out.print("系统消息：欢迎【" +
                user.getName()+
                "】加入聊天室【" + this.name + "】\n");
    }

    protected void deregister(User user) {
        users.remove(user);//用户注销，从列表中删除用户
    }

    protected abstract void sendMsg(User from, User to, String msg);
    protected abstract String processMsg(User from, User to, String msg);

}
