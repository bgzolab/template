package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class 剑指OfferII016不含重复字符的最长子字符串{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII016不含重复字符的最长子字符串().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int lengthOfLongestSubstring(String s) {
        HashMap<Character, Integer> hm = new HashMap<>();
        int ans=0,
        left=0,
        right=0,
        len=s.length();

        while(right<len){
            Character ch = s.charAt(right);
            hm.put(ch, hm.getOrDefault(ch, 0)+1);
//            System.out.print("ch: " + ch + ", hm.get(ch): " + hm.get(ch));

            while(left<=right && hm.get(ch) > 1){
                Character ch2 = s.charAt(left);
                hm.put(ch2, hm.get(ch2)-1);
//                System.out.print(", hm.get(s.charAt(left)): " + hm.get(s.charAt(left)));
//                System.out.print(", left: " + left);
//                System.out.println(", right: " + right);
                left++;
            }
//            System.out.println(", hm.get(ch): " + hm.get(ch));
            ans = Math.max(ans, right-left+1);
            right++;

        }
//        System.out.print(", finLeft: " + left);
//        System.out.println(", finRight: " + right);

        return ans;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 不含重复字符的最长子字符串
//给定一个字符串 s ，请你找出其中不含有重复字符的 最长连续子字符串 的长度。 
//
// 
//
// 示例 1: 
//
// 
//输入: s = "abcabcbb"
//输出: 3 
//解释: 因为无重复字符的最长子字符串是 "abc"，所以其长度为 3。
// 
//
// 示例 2: 
//
// 
//输入: s = "bbbbb"
//输出: 1
//解释: 因为无重复字符的最长子字符串是 "b"，所以其长度为 1。
// 
//
// 示例 3: 
//
// 
//输入: s = "pwwkew"
//输出: 3
//解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
//     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
// 
//
// 示例 4: 
//
// 
//输入: s = ""
//输出: 0
// 
//
// 
//
// 提示： 
//
// 
// 0 <= s.length <= 5 * 10⁴ 
// s 由英文字母、数字、符号和空格组成 
// 
//
// 
//
// 注意：本题与主站 3 题相同： https://leetcode-cn.com/problems/longest-substring-without-
//repeating-characters/ 
// Related Topics 哈希表 字符串 滑动窗口 👍 42 👎 0
