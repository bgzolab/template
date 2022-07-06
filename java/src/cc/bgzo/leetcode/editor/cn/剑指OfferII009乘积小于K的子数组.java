package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII009乘积小于K的子数组{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII009乘积小于K的子数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
//        1. 滑动窗口, 因为是连续的, 所以不用考虑2^n种情况, 每次往右滑1, 最多增加 i 个值,
//        在这基础上继续淘汰. via:https://leetcode.cn/problems/subarray-product-less-than-k/solution/cheng-ji-xiao-yu-k-de-zi-shu-zu-by-leetc-92wl/
        int ret = 0;
        int prod = 1, i = 0;

        for(int j=0; j<nums.length;j++){
            prod *= nums[j];
            while(i<=j && prod >= k){
                prod/=nums[i];
                i++;
            }
            ret += j-i+1;
        }
        return ret;
//        2. 二分, 实在是看不懂二分的思路, woc...
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 乘积小于 K 的子数组
//给定一个正整数数组 nums和整数 k ，请找出该数组内乘积小于 k 的连续的子数组的个数。 
//
// 
//
// 示例 1: 
//
// 
//输入: nums = [10,5,2,6], k = 100
//输出: 8
//解释: 8 个乘积小于 100 的子数组分别为: [10], [5], [2], [6], [10,5], [5,2], [2,6], [5,2,6]。
//需要注意的是 [10,5,2] 并不是乘积小于100的子数组。
// 
//
// 示例 2: 
//
// 
//输入: nums = [1,2,3], k = 0
//输出: 0 
//
// 
//
// 提示: 
//
// 
// 1 <= nums.length <= 3 * 10⁴ 
// 1 <= nums[i] <= 1000 
// 0 <= k <= 10⁶ 
// 
//
// 
//
// 注意：本题与主站 713 题相同：https://leetcode-cn.com/problems/subarray-product-less-than-
//k/ 
// Related Topics 数组 滑动窗口 👍 85 👎 0
