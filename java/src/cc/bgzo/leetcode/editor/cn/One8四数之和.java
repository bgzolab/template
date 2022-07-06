package cc.bgzo.leetcode.editor.cn;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class One8四数之和{
    public static void main(String[] args) {
        Solution solution = new One8四数之和().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public List<List<Integer>> fourSum(int[] nums, int target) {
        Arrays.sort(nums);
        return nSumTarget(Arrays.stream(nums).boxed().collect(Collectors.toList()),
                4, 0, target);
    }

        public List<List<Integer>> nSumTarget (List<Integer> nums,
                                               int n, int start, long target){
//        via: @labuladong & https://mp.weixin.qq.com/s/fSyJVvggxHq28a0SdmZm6Q
            // 会有 i 和 nums.get(i) 映射的问题.
//        nums.sort();
//        Collections.sort(nums);
            int size = nums.size();
            List<List<Integer>> res= new ArrayList<>();
            if( n < 2 || size < n) return res;

            if( n == 2){
                int lo = start, hi = size -1;
                while (lo<hi){
                    int left = nums.get(lo), right = nums.get(hi),
                            sum = left + right;

                    if(sum < target){
                        while (lo < hi && nums.get(lo) == left) lo++;
                    } else if( sum > target ){
                        while (lo < hi && nums.get(hi) == right) hi--;
                    }else {
                        res.add(new ArrayList<Integer>(){{add(left); add(right);}});

                        while (lo < hi && nums.get(lo) == left) lo++;
                        while (lo < hi && nums.get(hi)== right) hi--;
                    }
                }
            }else{
                for(int i = start; i < size; i++){
                    int now = nums.get(i);
                    List<List<Integer>> sub =
                            nSumTarget(nums, n-1, i+1, target-now);

                    for(List<Integer> arr: sub){
                        arr.add(now);
                        res.add(arr);
                    }

                    while ( i < size-1 && nums.get(i).equals(nums.get(i+1))) i++;
                    // More detail via: 15
                }
            }
            return res;
        }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 四数之和
//给你一个由 n 个整数组成的数组 nums ，和一个目标值 target 。请你找出并返回满足下述全部条件且不重复的四元组 [nums[a], nums[
//b], nums[c], nums[d]] （若两个四元组元素一一对应，则认为两个四元组重复）： 
//
// 
// 0 <= a, b, c, d < n 
// a、b、c 和 d 互不相同 
// nums[a] + nums[b] + nums[c] + nums[d] == target 
// 
//
// 你可以按 任意顺序 返回答案 。 
//
// 
//
// 示例 1： 
//
// 
//输入：nums = [1,0,-1,0,-2,2], target = 0
//输出：[[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
// 
//
// 示例 2： 
//
// 
//输入：nums = [2,2,2,2,2], target = 8
//输出：[[2,2,2,2]]
// 
//
// 
//
// 提示： 
//
// 
// 1 <= nums.length <= 200 
// -10⁹ <= nums[i] <= 10⁹ 
// -10⁹ <= target <= 10⁹ 
// 
// Related Topics 数组 双指针 排序 👍 1287 👎 0
