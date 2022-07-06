package cc.bgzo.leetcode.editor.cn;

import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class 剑指OfferII007数组中和为0的三个数{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII007数组中和为0的三个数().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public List<List<Integer>> threeSum(int[] nums) {
//        List<Integer> numbers = new ArrayList<Integer>(Arrays.asList(nums));

        Arrays.sort(nums);
        return nSumTarget(Arrays.stream(nums).boxed().collect(Collectors.toList()),
                3, 0, 0);
//        return nSumTarget2(nums, 3, 0, 0);
    }

    public List<List<Integer>> nSumTarget (List<Integer> nums,
                                         int n, int start, int target){
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
//                和 for 搭配, 少跳一步, 最后下一次for后直接可以补上, 就可以完整运行下去.
//                while ( i < size && nums.get(i) == now ) i++;
                // 这里需要在原数组中跳过-57553这两个相同的值, 因为其他两个元素被重复利用, 所以就会重复,
                // 但是第一个 while 为什么结果就不一样呢? 就可以跳过那个值呢? 因为是和外面 i++ 搭配的.
                //
                //[-29078,86631,-57553,]
                //[-28719,86272,-57553,]
                //[-18159,75712,-57553,]
                //[-15619,73172,-57553,]
                //[-14866,72419,-57553,]
                //[-10957,68510,-57553,]
                //[-9741,67294,-57553,]
                //[-5532,63085,-57553,]
                //[-1331,58884,-57553,]
                //[5465,52088,-57553,]
                //[19878,37675,-57553,]
                //[24520,33033,-57553,]
                //[25874,31679,-57553,]
                //[28007,29546,-57553,]
                //[-29078,86631,-57553,]
                //[-28719,86272,-57553,]
                //[-18159,75712,-57553,]
                //[-15619,73172,-57553,]
                //[-14866,72419,-57553,]
                //[-10957,68510,-57553,]
                //[-9741,67294,-57553,]
                //[-5532,63085,-57553,]
                //[-1331,58884,-57553,]
                //[5465,52088,-57553,]
                //[19878,37675,-57553,]
                //[24520,33033,-57553,]
                //[25874,31679,-57553,]
                //[28007,29546,-57553,]
                // FIXME: 不理解的是为什么 ArrayList 和  nums.get(i) == nums.get(i+1) 搭上
                // -57553就是跳不过... 传值和传引用的区别啊!!!!!! 艸艸艸艸!!!!!
                // Array == 两个元素比较值, ArrayList == 比较引用啊艸艸艸艸!!!!!
            }
        }
        return res;
    }

    public List<List<Integer>> nSumTarget2 (int[] nums,
                                            int n, int start, int target){
//        via: @labuladong & https://mp.weixin.qq.com/s/fSyJVvggxHq28a0SdmZm6Q
        int size = nums.length;
        List<List<Integer>> res= new ArrayList<>();
        if( n < 2 || size < n) return res;

        if( n == 2){
            int lo = start, hi = size -1;
            while (lo < hi){
                int left = nums[lo], right = nums[hi],
                        sum = left + right;

                if(sum < target){
                    while (lo < hi && nums[lo] == left) lo++;
                } else if( sum > target ){
                    while (lo < hi && nums[hi] == right) hi--;
                } else {
//                        List<Integer> numbers = new ArrayList<Integer>(Arrays.asList(nums));
//                        res.add(new ArrayList<Integer>(){{add(left); add(right);}});
                    res.add(new ArrayList<Integer>(Arrays.asList(left, right)));

                    while (lo < hi && nums[lo] == left) lo++;

                    while (lo < hi && nums[hi] == right) hi--;
                }

            }
        }else{
            for(int i = start; i < size; i++){
                int now = nums[i];

                List<List<Integer>> sub =
                        nSumTarget2(nums, n-1, i+1, target-nums[i]);

                for(List<Integer> arr: sub){
                    arr.add(nums[i]);
                    res.add(arr);
                }
                while (i < size-1 && nums[i]==nums[i+1]) i++;
//                while ( i < size && nums[i] == now ) i++;

            }
        }
        return res;
    }

}
//leetcode submit region end(Prohibit modification and deletion)

}
// 数组中和为 0 的三个数
//给定一个包含 n 个整数的数组 nums，判断 nums 中是否存在三个元素 a ，b ，c ，使得 a + b + c = 0 ？请找出所有和为 0 且 
//不重复 的三元组。 
//
// 
//
// 示例 1： 
//
// 
//输入：nums = [-1,0,1,2,-1,-4]
//输出：[[-1,-1,2],[-1,0,1]]
// 
//
// 示例 2： 
//
// 
//输入：nums = []
//输出：[]
// 
//
// 示例 3： 
//
// 
//输入：nums = [0]
//输出：[]
// 
//
// 
//
// 提示： 
//
// 
// 0 <= nums.length <= 3000 
// -10⁵ <= nums[i] <= 10⁵ 
// 
//
// 
//
// 注意：本题与主站 15 题相同：https://leetcode-cn.com/problems/3sum/ 
// Related Topics 数组 双指针 排序 👍 69 👎 0
