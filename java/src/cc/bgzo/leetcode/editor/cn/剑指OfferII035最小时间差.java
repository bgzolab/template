package cc.bgzo.leetcode.editor.cn;

import java.lang.reflect.Array;
import java.util.Collections;
import java.util.List;

public class 剑指OfferII035最小时间差{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII035最小时间差().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int findMinDifference(List<String> timePoints) {
        Collections.sort(timePoints);

        int size = timePoints.size(),
        min = Integer.MAX_VALUE;

//        1. failed 牛皮藓代码...
//        for(int lo=0, hi=1; hi<size; lo++, hi++){
//            int fi = Integer. parseInt(timePoints.get(lo).substring(0,2));
//            int se = Integer. parseInt(timePoints.get(lo).substring(3,5));
//
//            int th = Integer. parseInt(timePoints.get(hi).substring(0,2));
//            int fo = Integer. parseInt(timePoints.get(hi).substring(3,5));
//
////            System.out.println(fi+" "+ se+" "+th+" "+ fo);
//            if(fi==th) {
//                min = Math.min(min, Math.abs(se-fo));
//                continue;
//            }
//            min = Math.min(min, fi>th? (fi-th)*60+(se-fo):(th-fi)*60+(fo-se));
//
//            if(min > 720){
//                min = 1440-min;
//            }
//        }
        int t0Minutes = getMinutes(timePoints.get(0));
        int preMinutes = t0Minutes;
        for (int i = 1; i < timePoints.size(); ++i) {
            int minutes = getMinutes(timePoints.get(i));
            min = Math.min(min, minutes - preMinutes); // 相邻时间的时间差

            preMinutes = minutes;
        }
        min = Math.min(min, t0Minutes + 1440 - preMinutes); // 首尾时间的时间差
//        System.out.println(t0Minutes +" " + preMinutes);
        return min;
        // via: https://leetcode.cn/problems/569nqc/solution/zui-xiao-shi-jian-chai-by-leetcode-solut-ue5t/
    }
    public int getMinutes(String t) {
        return ((t.charAt(0) - '0') * 10 + (t.charAt(1) - '0')) * 60 + (t.charAt(3) - '0') * 10 + (t.charAt(4) - '0');
    }

}
//leetcode submit region end(Prohibit modification and deletion)

}
// 最小时间差
//给定一个 24 小时制（小时:分钟 "HH:MM"）的时间列表，找出列表中任意两个时间的最小时间差并以分钟数表示。 
//
// 
//
// 示例 1： 
//
// 
//输入：timePoints = ["23:59","00:00"]
//输出：1
// 
//
// 示例 2： 
//
// 
//输入：timePoints = ["00:00","23:59","00:00"]
//输出：0
// 
//
// 
//
// 提示： 
//
// 
// 2 <= timePoints <= 2 * 10⁴ 
// timePoints[i] 格式为 "HH:MM" 
// 
//
// 
//
// 注意：本题与主站 539 题相同： https://leetcode-cn.com/problems/minimum-time-difference/ 
// Related Topics 数组 数学 字符串 排序 👍 21 👎 0
