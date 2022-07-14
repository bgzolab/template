package cc.bgzo.leetcode.editor.cn;

import com.sun.xml.internal.ws.api.ha.HaInfo;

import java.util.*;

public class 剑指OfferII031最近最少使用缓存{
    public static void main(String[] args) {
        LRUCache solution = new 剑指OfferII031最近最少使用缓存().new LRUCache(0);
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class LRUCache extends LinkedHashMap<Integer, Integer> {

        private int capacity;

        public LRUCache(int capacity) {
            super(capacity, 0.75F, true);
            this.capacity = capacity;
        }

        public int get(int key) {
            return super.getOrDefault(key, -1);
        }

        public void put(int key, int value) {
            super.put(key, value);
        }

        @Override
        protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
            return size() > capacity;
        }//via：https://leetcode.cn/problems/OrIXps/solution/zui-jin-zui-shao-shi-yong-huan-cun-by-le-p3c2/


//    HashMap<Integer, Integer> hm;
//    HashMap<Integer, Long> time;
//    int size;
//
//    public LRUCache(int capacity) {
//        hm = new HashMap<>();
//        time = new HashMap<>();
//        size = capacity;
//    }
//
//    public int get(int key) {
//        if(hm.containsKey(key)){
//            long tmp = System.currentTimeMillis();
//            time.put(key, tmp);
//            System.out.println("get update" + key + ", " + tmp);
//            return hm.get(key);
////            for (Integer k : time.keySet()) {
////                System.out.print("k "+ k + ", time:" +time.get(k)+", ");
////            }
////            System.out.println("");
//        }
//        return -1;
//    }
//
//    public void put(int key, int value) {
//
//        if(time.containsKey(key)){
//            long tmp = System.currentTimeMillis();
//            time.put(key, tmp);
//            hm.put(key, value);
//            System.out.println("update" + key + ", " + System.currentTimeMillis());
//            return;
//        }
//
//        if(size > time.size()){
////            System.out.println("put" + key + ", " + value);
////            System.out.println("put" + key + ", " + System.currentTimeMillis());
//            long tmp = System.currentTimeMillis();
//            time.put(key, tmp);
//            hm.put(key, value);
//            System.out.println("nowTime "+System.currentTimeMillis()+" and my key time: "+time.get(key));
//            return;
//        }
//
//        int min = 0;
//        long minTime=Long.MAX_VALUE;
//        for (Integer k : time.keySet()) {
//            System.out.print("k:"+ k + ", time:" +time.get(k)+", ");
//            if(time.get(k) < minTime) {
//                minTime = time.get(k);
//                min = k;
////                System.out.println("minTime" + minTime + "time " + time.get(k) + ", min " + min);
//            }
//        }
//        System.out.println("");
//
//        /**
//         *  加入时间太快比较不了啊!!!
//         *      put 1: 1657797549811 and my key time: 1657797549811
//         * 		put 2: 1657797549828 and my key time: 1657797549828
//         * 		get update1, 1657797549828
//         * 		k:1, time:1657797549828, k:2, time:1657797549828,
//         * 	// 为什么这三个时间是一样的 ???
//         * 		get update2, 1657797549841
//         * 		k:2, time:1657797549841, k:3, time:1657797549841,
//         * 		get update3, 1657797549841
//         * 		get update4, 1657797549841
//         * */
//
//        time.remove(min);
//        hm.remove(min);
//
//        long tmp = System.currentTimeMillis();
//        time.put(key, tmp);
//        hm.put(key, value);
//    }
}

/**
 * Your LRUCache object will be instantiated and called as such:
 * LRUCache obj = new LRUCache(capacity);
 * int param_1 = obj.get(key);
 * obj.put(key,value);
 */
//leetcode submit region end(Prohibit modification and deletion)

}
// 最近最少使用缓存
//
// 运用所掌握的数据结构，设计和实现一个 LRU (Least Recently Used，最近最少使用) 缓存机制 。 
//
// 实现 LRUCache 类： 
//
// 
// LRUCache(int capacity) 以正整数作为容量 capacity 初始化 LRU 缓存 
// int get(int key) 如果关键字 key 存在于缓存中，则返回关键字的值，否则返回 -1 。 
// void put(int key, int value) 如果关键字已经存在，则变更其数据值；如果关键字不存在，则插入该组「关键字-值」。当缓存容量达到上
//限时，它应该在写入新数据之前删除最久未使用的数据值，从而为新的数据值留出空间。 
// 
//
// 
//
// 示例： 
//
// 
//输入
//["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
//[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
//输出
//[null, null, null, 1, null, -1, null, -1, 3, 4]
//
//解释
//LRUCache lRUCache = new LRUCache(2);
//lRUCache.put(1, 1); // 缓存是 {1=1}
//lRUCache.put(2, 2); // 缓存是 {1=1, 2=2}
//lRUCache.get(1);    // 返回 1
//lRUCache.put(3, 3); // 该操作会使得关键字 2 作废，缓存是 {1=1, 3=3}
//lRUCache.get(2);    // 返回 -1 (未找到)
//lRUCache.put(4, 4); // 该操作会使得关键字 1 作废，缓存是 {4=4, 3=3}
//lRUCache.get(1);    // 返回 -1 (未找到)
//lRUCache.get(3);    // 返回 3
//lRUCache.get(4);    // 返回 4
// 
//
// 
//
// 提示： 
//
// 
// 1 <= capacity <= 3000 
// 0 <= key <= 10000 
// 0 <= value <= 10⁵ 
// 最多调用 2 * 10⁵ 次 get 和 put 
// 
// 
//
// 
//
// 进阶：是否可以在 O(1) 时间复杂度内完成这两种操作？ 
//
// 
//
// 注意：本题与主站 146 题相同：https://leetcode-cn.com/problems/lru-cache/ 
// Related Topics 设计 哈希表 链表 双向链表 👍 55 👎 0
