package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class 剑指OfferII010和为K的子数组{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII010和为K的子数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int subarraySum(int[] nums, int k) {
        HashMap<Integer, Integer> hm = new HashMap<>();
        hm.put(0, 1);
        int sum = 0, ans=0;

        for(int i =0 ;i<nums.length;i++){
            sum+=nums[i];

            if(hm.containsKey(sum-k)){
                ans += hm.get(sum-k);
            }
//            hm.put(i, hm.getOrDefault(i,1));
            hm.put(sum, hm.getOrDefault(sum,0)+1);
        }
        return ans;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 和为 k 的子数组
//给定一个整数数组和一个整数 k ，请找到该数组中和为 k 的连续子数组的个数。 
//
// 
//
// 示例 1： 
//
// 
//输入:nums = [1,1,1], k = 2
//输出: 2
//解释: 此题 [1,1] 与 [1,1] 为两种不同的情况
// 
//
// 示例 2： 
//
// 
//输入:nums = [1,2,3], k = 3
//输出: 2
// 
//
// 
//
// 提示: 
//
// 
// 1 <= nums.length <= 2 * 10⁴ 
// -1000 <= nums[i] <= 1000 
// 
// -10⁷ <= k <= 10⁷ 
// 
// 
//
// 
//
// 注意：本题与主站 560 题相同： https://leetcode-cn.com/problems/subarray-sum-equals-k/ 
// Related Topics 数组 哈希表 前缀和 👍 85 👎 0
