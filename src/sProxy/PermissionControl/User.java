package sProxy.PermissionControl;

/* File Name: User
 * Author: bGZo
 * Created Time: 10/19/2022 21:25
 * License: MIT
 * Description:
 */
public class User {
    private String name;
    protected Permission permission;

    public User() {
        name = "Default User";
        permission = new Permission(0);
    }
    public User(String name, Permission permission) {
        this.name = name;
        this.permission = permission;
    }

    public void setName(String name) { this.name = name; }
    public String getName() { return name; }

    public void on(){ permission.setLevel(1);}
    public void off(){ permission.setLevel(0); }

    public void status(){
        switch (permission.getLevel()){
            case 0: System.out.println(name + " is OFF"); break;
            case 1: System.out.println(name + " is ON"); break;
        }
    }

}
