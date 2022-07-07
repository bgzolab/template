package cc.bgzo.leetcode.editor.cn;
public class Seven13乘积小于K的子数组{
    public static void main(String[] args) {
        Solution solution = new Seven13乘积小于K的子数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int numSubarrayProductLessThanK(int[] nums, int k) {
        int l=0, r=0, sum=1, ret=0;
        while (r<nums.length){
            sum*=nums[r];
            while (l<=r && sum>=k){ // NOTE: l&j 的关系必须要考虑到
                sum/=nums[l];
                l++;
            }
            ret += r-l+1;
            r++;
        }
        return ret;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 乘积小于 K 的子数组
//给你一个整数数组 nums 和一个整数 k ，请你返回子数组内所有元素的乘积严格小于 k 的连续子数组的数目。
// 
//
// 示例 1： 
//
// 
//输入：nums = [10,5,2,6], k = 100
//输出：8
//解释：8 个乘积小于 100 的子数组分别为：[10]、[5]、[2],、[6]、[10,5]、[5,2]、[2,6]、[5,2,6]。
//需要注意的是 [10,5,2] 并不是乘积小于 100 的子数组。
// 
//
// 示例 2： 
//
// 
//输入：nums = [1,2,3], k = 0
//输出：0 
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
// Related Topics 数组 滑动窗口 👍 570 👎 0
