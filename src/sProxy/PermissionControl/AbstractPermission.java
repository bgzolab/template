package sProxy.PermissionControl;

/* File Name: AbstractPermission
 * Author: bGZo
 * Created Time: 10/19/2022 21:12
 * License: MIT
 * Description:
 */
public interface AbstractPermission {

    public void modifyInfo();

    public void view();

    public void post();

    public void modifyPost();

    public void setLevel(int level);

}
