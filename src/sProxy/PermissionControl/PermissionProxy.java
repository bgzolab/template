package sProxy.PermissionControl;

/* File Name: PermissionProxy
 * Author: bGZo
 * Created Time: 10/19/2022 21:15
 * License: MIT
 * Description:
 */
public class PermissionProxy implements AbstractPermission{
    private User user;

    public PermissionProxy(User user) {
        this.user = user;
    }

    @Override
    public void modifyInfo() {
        switch (user.permission.getLevel()){
            case 0: System.out.println("Permission Denied.");break;
            case 1: user.permission.modifyPost(); break;
        }
    }

    @Override
    public void view() {
        // Guest could view as well.
        user.permission.view();
    }

    @Override
    public void post() {
        switch (user.permission.getLevel()){
            case 0: System.out.println("Permission Denied.");break;
            case 1: user.permission.post(); break;
        }
    }

    @Override
    public void modifyPost() {
        switch (user.permission.getLevel()){
            case 0: System.out.println("Permission Denied.");break;
            case 1: user.permission.modifyPost(); break;
        }
    }

    @Override
    public void setLevel(int level) {
        switch (user.permission.getLevel()){
            case 0: System.out.println("Permission Denied.");break;
            case 1: user.permission.setLevel(level); break;
        }
    }
}
