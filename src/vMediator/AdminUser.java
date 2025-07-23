package vMediator;

/* File Name: AdminUser
 * Author: bGZo
 * Created Time: 6/24/2022 12:30
 * License: MIT
 * Description:
 */
public class AdminUser extends User{
    public AdminUser(String name) {
        super(name);
    }

    public void kick(User user) {       //踢出其他用户
        user.logout();
    }
}
