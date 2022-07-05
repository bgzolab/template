package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class One两数之和{
    public static void main(String[] args) {
        Solution solution = new One两数之和().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int[] twoSum(int[] numbers, int target) {
        HashMap<Integer, Integer> hm = new HashMap<>();
        for(int i = 0; i<numbers.length; i++){

            if(hm.containsKey(target-numbers[i]) )
                // NOTE: 可以保证 i != hm.get(target-numbers[i])
                // 因为每个元素只能访问一遍, 第一次不存在直接不会返回结果
                return new int[]{hm.get(target-numbers[i]), i};

            hm.put(numbers[i], i);
        }

        return new int[]{};
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 两数之和
//给定一个整数数组 numbers 和一个整数目标值 target，请你在该数组中找出 和为目标值 target 的那 两个 整数，并返回它们的数组下标。 
//
// 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素在答案里不能重复出现。 
//
// 你可以按任意顺序返回答案。 
//
// 
//
// 示例 1： 
//
// 
//输入：numbers = [2,7,11,15], target = 9
//输出：[0,1]
//解释：因为 numbers[0] + numbers[1] == 9 ，返回 [0, 1] 。
// 
//
// 示例 2： 
//
// 
//输入：numbers = [3,2,4], target = 6
//输出：[1,2]
// 
//
// 示例 3： 
//
// 
//输入：numbers = [3,3], target = 6
//输出：[0,1]
// 
//
// 
//
// 提示： 
//
// 
// 2 <= numbers.length <= 10⁴ 
// -10⁹ <= numbers[i] <= 10⁹ 
// -10⁹ <= target <= 10⁹ 
// 只会存在一个有效答案 
// 
//
// 进阶：你可以想出一个时间复杂度小于 O(n²) 的算法吗？ 
// Related Topics 数组 哈希表 👍 14750 👎 0
