package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.atomic.AtomicReference;

public class 剑指OfferII004{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII004().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int singleNumber(int[] numbers) {
        HashMap<Integer, Integer> map = new HashMap<>();

        for(int i:numbers){
            if(!map.containsKey(i)) map.put(i, 1);
            else map.put(i, map.get(i) + 1);
        }

//        for(Integer i: map.keySet())
//            if(map.get(i) == 1) return i;

        for(Map.Entry<Integer, Integer> entry: map.entrySet()){
            if(entry.getValue() == 1) return entry.getKey();
        }


//        map.forEach((k,v)->{
//            if(v==1) {
//                System.out.println(k);
//                return;
//            }
//        }); forEach Lambda 不可以传出副作用, 离开作用域就无效了. 查到的例子全是打印输出的...
//        more https://stackoverflow.com/questions/23308193/break-or-return-from-java-8-stream-foreach
//        https://stackoverflow.com/questions/23407014/return-from-lambda-foreach-in-java
//        https://stackoverflow.com/questions/3571352/how-to-convert-integer-to-int
        return -1;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 只出现一次的数字 
//给你一个整数数组 numbers ，除某个元素仅出现 一次 外，其余每个元素都恰出现 三次 。请你找出并返回那个只出现了一次的元素。 
//
// 
//
// 示例 1： 
//
// 
//输入：numbers = [2,2,3,2]
//输出：3
// 
//
// 示例 2： 
//
// 
//输入：numbers = [0,1,0,1,0,1,100]
//输出：100
// 
//
// 
//
// 提示： 
//
// 
// 1 <= numbers.length <= 3 * 10⁴ 
// -2³¹ <= numbers[i] <= 2³¹ - 1 
// numbers 中，除某个元素仅出现 一次 外，其余每个元素都恰出现 三次 
// 
//
// 
//
// 进阶：你的算法应该具有线性时间复杂度。 你可以不使用额外空间来实现吗？ 
//
// 
//
// 注意：本题与主站 137 题相同：https://leetcode-cn.com/problems/single-number-ii/ 
// Related Topics 位运算 数组 👍 82 👎 0
