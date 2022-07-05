package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class One67两数之和II输入有序数组{
    public static void main(String[] args) {
        Solution solution = new One67两数之和II输入有序数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int[] twoSum(int[] numbers, int target) {

//        HashMap<Integer, Integer> hm =new HashMap<>();
//        for(int i = 0; i<numbers.length; i++){
//            if( hm.containsKey(target - numbers[i]) )
//                // NOTE: NOT target - numbers[i] != numbers[i] (数字不能重用)
//                // 是相同位置的数字不能重用
//                return new int[]{hm.get(target - numbers[i])+1, i+1};
//
//            hm.put(numbers[i], i);
//        }
//        return new int[]{};

//        3. double point
        int l = 0, r = numbers.length-1,
                left = numbers[l], right = numbers[r],
                find = target - left;

        while(l < r){

            while( right >= find ){
                if(left + right == target)
                    // NOTE: 此时一定有结论 l!=r (题设保证)
                    return new int[]{l+1, r+1};
                right = numbers[--r];
            }
            left = numbers[++l];
            find = target - left;
        }

        return new int[]{};
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 两数之和 II - 输入有序数组
//给你一个下标从 1 开始的整数数组 numbers ，该数组已按 非递减顺序排列 ，请你从数组中找出满足相加之和等于目标数 target 的两个
//数。
//如果
//设这
//两个数分别是 numbers[index1] 和 numbers[index2] ，则 1 <= index1 < index2 <= 
//numbers.
//
//length 。 
//
// 以长度为 2 的整数数组 [index1, index2] 的形式返回这两个整数的下标 index1 和 index2。 
//
// 你可以假设每个输入 只对应唯一的答案 ，而且你 不可以 重复使用相同的元素。 
//
// 你所设计的解决方案必须只使用常量级的额外空间。 
// 
//
// 示例 1： 
//
// 
//输入：numbers = [2,7,11,15], target = 9
//输出：[1,2]
//解释：2 与 7 之和等于目标数 9 。因此 index1 = 1, index2 = 2 。返回 [1, 2] 。 
//
// 示例 2： 
//
// 
//输入：numbers = [2,3,4], target = 6
//输出：[1,3]
//解释：2 与 4 之和等于目标数 6 。因此 index1 = 1, index2 = 3 。返回 [1, 3] 。 
//
// 示例 3： 
//
// 
//输入：numbers = [-1,0], target = -1
//输出：[1,2]
//解释：-1 与 0 之和等于目标数 -1 。因此 index1 = 1, index2 = 2 。返回 [1, 2] 。
// 
//
// 
//
// 提示： 
//
// 
// 2 <= numbers.length <= 3 * 10⁴ 
// -1000 <= numbers[i] <= 1000 
// numbers 按 非递减顺序 排列 
// -1000 <= target <= 1000 
// 仅存在一个有效答案 
// 
// Related Topics 数组 双指针 二分查找 👍 834 👎 0
