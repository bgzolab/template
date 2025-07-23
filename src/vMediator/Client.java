package vMediator;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/24/2022 10:06
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        ChatRoom chatRoom = new PublicChatRoom("设计模式");
//
        User user3 = new User("张三");
        User user4 = new User("李四");
        User user5 = new User("王五");
//
        user3.login(chatRoom);
        user4.login(chatRoom);
        user3.talk(null,"你好，四兄弟，就你一个在啊？");
        user4.talk(user3, "是啊，三哥。");
        user5.login(chatRoom);
        user3.talk(null, "瞧，王老五来了。");
    }
}
