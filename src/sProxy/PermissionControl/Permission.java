package sProxy.PermissionControl;

/* File Name: Permission
 * Author: bGZo
 * Created Time: 10/19/2022 21:16
 * License: MIT
 * Description:
 */
public class Permission implements AbstractPermission{
    private int level;

    public Permission() {
        level=0;
    }
    public Permission(int level) {
        this.level = level;
    }

    public int getLevel() {
        return level;
    }

    @Override
    public void setLevel(int level) {
        this.level = level;
        System.out.println("Set level successful");
    }

    @Override
    public void modifyInfo() {
        // TODO:  ... Change self info ...
        System.out.println("Change self info successful");
    }

    @Override
    public void view() {
        //TODO: ... Get post info and views ...
        System.out.println("Get post info successful");
    }

    @Override
    public void post() {
        //TODO: ... Send posts...
        System.out.println("Send posts successful");
    }

    @Override
    public void modifyPost() {
        //TODO: Modify self post
        System.out.println("Change self post successful");
    }

}
