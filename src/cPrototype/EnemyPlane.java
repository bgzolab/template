package cPrototype;

/* File Name: EnemyPlane
 * Author: bGZo
 * Created Time: 8/28/2022 01:39
 * License: MIT
 * Description:
 */
public class EnemyPlane implements Cloneable{
    private int x;
    private int y = 0;
//    private Bullet bullet;
//     子弹需要深拷贝, 因为不同敌机的子弹是不同的

    public EnemyPlane(int x){
        this.x = x;
    }

//    public EnemyPlane(int x, Bullet bullet){
//        this.x = x;
//        this.bullet = bullet;
//    }

    public int getX() {
        return x;
    }
    public int getY() {
        return y;
    }

    /**
     * 敌机飞
     */
    public void fly(){
        y++;
    }

    /**
     * 使得 Clone 后的实例可以再次修改横坐标.
     * @param x
     */
    public void setX(int x) {
        this.x = x;
    }

    @Override
    public EnemyPlane clone() throws CloneNotSupportedException {
        return (EnemyPlane) super.clone();
    }

//    @Override
//    protected EnemyPlane clone() throws CloneNotSupportedException {
//        EnemyPlane clonePlane = (EnemyPlane) super.clone();
//        clonePlane.setBullet = (this.bullet.clone());
//        // Bullet 也需要实现拷贝接口
//        return clonePlane;
//    }

}
