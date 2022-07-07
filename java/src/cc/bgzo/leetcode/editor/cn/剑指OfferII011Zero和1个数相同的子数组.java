package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class 剑指OfferII011Zero和1个数相同的子数组{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII011Zero和1个数相同的子数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int findMaxLength(int[] nums) {
        HashMap<Integer, Integer> hm = new HashMap<>();
        hm.put(0, -1);
//        int pre[]=new int[nums.length+1];
        int pre=0, max=0;
        for (int i=0;i<nums.length;i++){
            pre += (nums[i]==0)? -1:1;

            if(hm.containsKey(pre)){
                max=Math.max(max, i-hm.get(pre));
            }else {
                hm.put(pre, i);
            }
        }
        return max;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 0 1 1 0 1 1 1 0 0
// 0 和 1 个数相同的子数组
//给定一个二进制数组 nums , 找到含有相同数量的 0 和 1 的最长连续子数组，并返回该子数组的长度。 
//
// 
//
// 示例 1： 
//
// 
//输入: nums = [0,1]
//输出: 2
//说明: [0, 1] 是具有相同数量 0 和 1 的最长连续子数组。 
//
// 示例 2： 
//
// 
//输入: nums = [0,1,0]
//输出: 2
//说明: [0, 1] (或 [1, 0]) 是具有相同数量 0 和 1 的最长连续子数组。 
//
// 
//
// 提示： 
//
// 
// 1 <= nums.length <= 10⁵ 
// nums[i] 不是 0 就是 1 
// 
//
// 
//
// 注意：本题与主站 525 题相同： https://leetcode-cn.com/problems/contiguous-array/ 
// Related Topics 数组 哈希表 前缀和 👍 75 👎 0
