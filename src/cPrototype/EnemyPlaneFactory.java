package cPrototype;

/* File Name: EnemyPlaneFactory
 * Author: bGZo
 * Created Time: 8/28/2022 01:50
 * License: MIT
 * Description:
 */
public class EnemyPlaneFactory {
    public static EnemyPlane protoType = new EnemyPlane(200);

    public static EnemyPlane getInstance(int x) throws CloneNotSupportedException {

        /**
         * 复制原型机
         */
        EnemyPlane clone = protoType.clone();

        clone.setX(x);
        return clone;
    }
}
