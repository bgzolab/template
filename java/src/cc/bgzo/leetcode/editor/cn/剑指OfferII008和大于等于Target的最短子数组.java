package cc.bgzo.leetcode.editor.cn;

import java.lang.reflect.Array;
import java.util.Arrays;

public class 剑指OfferII008和大于等于Target的最短子数组{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII008和大于等于Target的最短子数组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int minSubArrayLen(int target, int[] nums) {
//        1. 模拟
//        int []sums = new int[nums.length];
//        int sum = 0, min = Integer.MAX_VALUE;
//
//        for(int i = 0; i<nums.length; i++){
//            sum += nums[i];
//            sums[i] = sum;
//
//            if(sum < target) {
//                if(i == nums.length - 1) return 0;
//                continue;
//            }
//            else if (sum == target) {
//                min = Math.min(min, i + 1);
//                continue;
//            }
//            int idx = i, tar = sum - target;
//            while (idx >= 0 && sums[idx] > tar){
//                idx--;
//            }
//            min = Math.min(min, i - idx);
//            System.out.println("i:" + i +", idx: " + idx);
//            return min;

//        2. sum + binary_search
//        int []sums = new int[nums.length + 1];
//        int sum = 0, min = Integer.MAX_VALUE;
//
//        for(int i = 1; i <= nums.length; i++)
//            sums[i] = sums[i-1] + nums[i-1];
//
//        for(int i = 1; i<= nums.length; i++){
//            int tar = target + sums[i-1];
////             sums[bound] - sum[i] >= target
////                      sums[bound] >= target + sum[i]
//
//            int bound = Arrays.binarySearch(sums, tar);
//
//            if(bound < 0){
//                bound = -bound - 1;
//            }
//            if(bound <=nums.length ){
//                min = Math.min(min, bound-(i-1));
//            }
//        }
//        return min==Integer.MAX_VALUE? 0: min;

//        3. sliding windows
        int left=0, right=0, sum = 0;
        int min = Integer.MAX_VALUE;

        while(right < nums.length){
            sum += nums[right];

            while (sum >= target){ // NOTE: NOTE sum > target
                min = Math.min(min, right-left + 1 ); // NOTE: NOT right-left
                sum -= nums[left];
                left ++;

            }
            right++;
        }

        return min==Integer.MAX_VALUE?0:min;
    }

//    int lowerBound(int []sums, int tar){
//
//    }

}
//leetcode submit region end(Prohibit modification and deletion)

}
// 和大于等于 target 的最短子数组
//给定一个含有 n 个正整数的数组和一个正整数 target 。 
//
// 找出该数组中满足其和 ≥ target 的长度最小的 连续子数组 [numsl, numsl+1, ..., numsr-1, numsr] ，并返回其长
//度。如果不存在符合条件的子数组，返回 0 。 
//
// 
//
// 示例 1： 
//
// 
//输入：target = 7, nums = [2,3,1,2,4,3]
// [2 , 5, 6, 8, 12 ,15]
//输出：2
//解释：子数组 [4,3] 是该条件下的长度最小的子数组。
// 
//
// 示例 2： 
//
// 
//输入：target = 4, nums = [1,4,4]
//输出：1
// 
//
// 示例 3： 
//
// 
//输入：target = 11, nums = [1,1,1,1,1,1,1,1]
//输出：0
// 
//
// 
//
// 提示： 
//
// 
// 1 <= target <= 10⁹ 
// 1 <= nums.length <= 10⁵ 
// 1 <= nums[i] <= 10⁵ 
// 
//
// 
//
// 进阶： 
//
// 
// 如果你已经实现 O(n) 时间复杂度的解法, 请尝试设计一个 O(n log(n)) 时间复杂度的解法。 
// 
//
// 
//
// 注意：本题与主站 209 题相同：https://leetcode-cn.com/problems/minimum-size-subarray-sum/ 
//
// Related Topics 数组 二分查找 前缀和 滑动窗口 👍 73 👎 0
