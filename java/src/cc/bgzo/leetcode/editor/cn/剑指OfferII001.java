package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII001{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII001().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int divide(int a, int b) {
        // 考虑被除数为最小值的情况
        if (a == Integer.MIN_VALUE) {
            if (b == 1) {
                return Integer.MIN_VALUE;
            }
            if (b == -1) {
                return Integer.MAX_VALUE;
            }
        }
        // 考虑除数为最小值的情况
        if (b == Integer.MIN_VALUE) {
            return a == Integer.MIN_VALUE ? 1 : 0;
        }
        // 考虑被除数为 0 的情况
        if (a == 0) {
            return 0;
        }

        // 一般情况，使用二分查找
        // find z: Z × Y ≥ X > ( Z + 1 ) × Y
        // 将所有的正数取相反数，这样就只需要考虑一种情况
        boolean rev = false;
        if (a > 0) {
            a = -a;
            rev = !rev;
        }
        if (b > 0) {
            b = -b;
            rev = !rev;
        }

        int left = 1, right = Integer.MAX_VALUE, ans = 0;
        while (left <= right) {
            // 注意溢出，并且不能使用除法
            int mid = left + ((right - left) >> 1);
            boolean check = quickAdd(b, mid, a);
            if (check) {
                ans = mid;
                // 注意溢出
                System.out.print(", mid: " + mid);

                if (mid == Integer.MAX_VALUE) {
                    break;
                }
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return rev ? -ans : ans;
    }

    // 快速乘
    public boolean quickAdd(int y, int z, int x) {
        // x 和 y 是负数，z 是正数, 判断 z * y >= x 是否成立
        // 换成正数就是判断 z * y < x
        int result = 0, add = y;
         while (z != 0) {
             if ((z & 1) != 0) {
                 if (result < x - add) { // 保证 result + add >= x
                     return false;
                 }
                 result += add;
             }
             if (z != 1) {
                 // z == 1 的时候就不可以加倍地加了.
                 // 只能加一次然后就退出去了
                 System.out.print("add: " + add);
                 System.out.print(", x: " + x);
                 System.out.print(", result: " + x);
                 System.out.println(", z: " + z);

                 if (add < x - add) {// 保证 add + add >= x
                     // NOTE: 这里是负数 是反着来的
                     // 换算成正数 就是 add 始终保持 x 的一半以下
                     return false;
                 }

                 System.out.println("add: " + add);
                 System.out.println("x: " + x);
                 System.out.println("result: " + x);
                 add += add;
             }
             z >>= 1;
         }
         return true;
    }
    //via: https://leetcode.cn/problems/xoh6Oh/solution/zheng-shu-chu-fa-by-leetcode-solution-3572
        /*
input: 15 2
add: -2, x: -15, result: -15, z: 1073741824
add: -4, x: -15, result: -15, z: 536870912
add: -8, x: -15, result: -15, z: 268435456
add: -2, x: -15, result: -15, z: 536870912
add: -4, x: -15, result: -15, z: 268435456
add: -8, x: -15, result: -15, z: 134217728
add: -2, x: -15, result: -15, z: 268435456
add: -4, x: -15, result: -15, z: 134217728
add: -8, x: -15, result: -15, z: 67108864
add: -2, x: -15, result: -15, z: 134217728
add: -4, x: -15, result: -15, z: 67108864
add: -8, x: -15, result: -15, z: 33554432
add: -2, x: -15, result: -15, z: 67108864
add: -4, x: -15, result: -15, z: 33554432
add: -8, x: -15, result: -15, z: 16777216
add: -2, x: -15, result: -15, z: 33554432
add: -4, x: -15, result: -15, z: 16777216
add: -8, x: -15, result: -15, z: 8388608
add: -2, x: -15, result: -15, z: 16777216
add: -4, x: -15, result: -15, z: 8388608
add: -8, x: -15, result: -15, z: 4194304
add: -2, x: -15, result: -15, z: 8388608
add: -4, x: -15, result: -15, z: 4194304
add: -8, x: -15, result: -15, z: 2097152
add: -2, x: -15, result: -15, z: 4194304
add: -4, x: -15, result: -15, z: 2097152
add: -8, x: -15, result: -15, z: 1048576
add: -2, x: -15, result: -15, z: 2097152
add: -4, x: -15, result: -15, z: 1048576
add: -8, x: -15, result: -15, z: 524288
add: -2, x: -15, result: -15, z: 1048576
add: -4, x: -15, result: -15, z: 524288
add: -8, x: -15, result: -15, z: 262144
add: -2, x: -15, result: -15, z: 524288
add: -4, x: -15, result: -15, z: 262144
add: -8, x: -15, result: -15, z: 131072
add: -2, x: -15, result: -15, z: 262144
add: -4, x: -15, result: -15, z: 131072
add: -8, x: -15, result: -15, z: 65536
add: -2, x: -15, result: -15, z: 131072
add: -4, x: -15, result: -15, z: 65536
add: -8, x: -15, result: -15, z: 32768
add: -2, x: -15, result: -15, z: 65536
add: -4, x: -15, result: -15, z: 32768
add: -8, x: -15, result: -15, z: 16384
add: -2, x: -15, result: -15, z: 32768
add: -4, x: -15, result: -15, z: 16384
add: -8, x: -15, result: -15, z: 8192
add: -2, x: -15, result: -15, z: 16384
add: -4, x: -15, result: -15, z: 8192
add: -8, x: -15, result: -15, z: 4096
add: -2, x: -15, result: -15, z: 8192
add: -4, x: -15, result: -15, z: 4096
add: -8, x: -15, result: -15, z: 2048
add: -2, x: -15, result: -15, z: 4096
add: -4, x: -15, result: -15, z: 2048
add: -8, x: -15, result: -15, z: 1024
add: -2, x: -15, result: -15, z: 2048
add: -4, x: -15, result: -15, z: 1024
add: -8, x: -15, result: -15, z: 512
add: -2, x: -15, result: -15, z: 1024
add: -4, x: -15, result: -15, z: 512
add: -8, x: -15, result: -15, z: 256
add: -2, x: -15, result: -15, z: 512
add: -4, x: -15, result: -15, z: 256
add: -8, x: -15, result: -15, z: 128
add: -2, x: -15, result: -15, z: 256
add: -4, x: -15, result: -15, z: 128
add: -8, x: -15, result: -15, z: 64
add: -2, x: -15, result: -15, z: 128
add: -4, x: -15, result: -15, z: 64
add: -8, x: -15, result: -15, z: 32
add: -2, x: -15, result: -15, z: 64
add: -4, x: -15, result: -15, z: 32
add: -8, x: -15, result: -15, z: 16
add: -2, x: -15, result: -15, z: 32
add: -4, x: -15, result: -15, z: 16
add: -8, x: -15, result: -15, z: 8
add: -2, x: -15, result: -15, z: 16
add: -4, x: -15, result: -15, z: 8
add: -8, x: -15, result: -15, z: 4
add: -2, x: -15, result: -15, z: 8
add: -4, x: -15, result: -15, z: 4
add: -8, x: -15, result: -15, z: 2
add: -2, x: -15, result: -15, z: 4
add: -4, x: -15, result: -15, z: 2
add: -8, x: -15, result: -15, z: 1, mid: 4
add: -2, x: -15, result: -15, z: 6
add: -4, x: -15, result: -15, z: 3
add: -8, x: -15, result: -15, z: 1, mid: 6
add: -2, x: -15, result: -15, z: 7
add: -4, x: -15, result: -15, z: 3
add: -8, x: -15, result: -15, z: 1, mid: 7
        * */
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 整数除法
//English description is not available for the problem. Please switch to 
//Chinese. Related Topics 位运算 数学 👍 160 👎 0
