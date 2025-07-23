package sProxy.PermissionControl;

/* File Name: Client
 * Author: bGZo
 * Created Time: 10/19/2022 21:29
 * License: MIT
 * Description:  via: https://blog.csdn.net/qq_45703570/article/details/123812750
    * Origin: 把 Permission 直接放在 PermissionProxy 中, 没有用户的存在.
    * Modify: 修改后把 Permission 放在 User 中, 然后把 User 放在 PermissionProxy 中实现代理
 */

public class Client {
    public static void main(String[] args) {
        User user = new User(
                "WjR",
                new Permission(0)
        );

        PermissionProxy permissionProxy = new PermissionProxy(user);

        user.off(); user.status();

        permissionProxy.modifyInfo();
        permissionProxy.view();
        permissionProxy.post();
        permissionProxy.modifyPost();

        user.on(); user.status();

        permissionProxy.modifyInfo();
        permissionProxy.view();
        permissionProxy.post();
        permissionProxy.modifyPost();

    }
}
