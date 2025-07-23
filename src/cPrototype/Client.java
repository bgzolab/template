package cPrototype;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/* File Name: Client
 * Author: bGZo
 * Created Time: 8/28/2022 01:44
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        List<EnemyPlane> enemyPlanes = new ArrayList<>();

//        for (int i = 0; i < 500; i++) {
//            EnemyPlane ep = new EnemyPlane(new Random().nextInt());
//            enemyPlanes.add(ep);
//            // 效率非常低, 开局就一次性全部加载好是对资源的浪费 --> 懒加载 --> 性能瓶颈 new --> 支持原型拷贝
//        }

        EnemyPlaneFactory enemyPlaneFactory = new EnemyPlaneFactory();

        // 代码中使用原型工厂实例化对象
        // ......

    }
}
