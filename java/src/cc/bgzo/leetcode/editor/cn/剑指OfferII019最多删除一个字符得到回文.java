package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII019最多删除一个字符得到回文{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII019最多删除一个字符得到回文().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean validPalindrome(String s) {
//        for(int i=0; i<s.length(); i++){
//            if(isPalindrome(s.substring(0, i) + s.substring(i+1, s.length()))){
//                System.out.println();
//                return true;
//            }
//        }
//        return false;
//    boolean isPalindrome(String i){
//        int lo=0, hi = i.length()-1;
//        while (lo<=hi){
//            if(i.charAt(lo)!=i.charAt(hi)) return false;
//            lo++;
//            hi--;
//        }
//        return true;
//    }

        int lo=0, hi = s.length()-1;
        boolean flag = true;

        while (lo<=hi){
            if(s.charAt(lo)!=s.charAt(hi)) {
                flag =false;
                break;
            }
            lo++;
            hi--;
        }

        if(flag) return true;
        return isPalindrome(s, lo) || isPalindrome(s,hi);
    }

    boolean isPalindrome(String s, int index){
        int lo=0, hi = s.length()-1;
        while (lo<=hi){
            if(lo == index)lo++;
            if(hi == index)hi--;

            if(s.charAt(lo)!=s.charAt(hi)) return false;
            lo++;
            hi--;
        }
        return true;
    }

/*
* aguokepatgbnvfqmgmlcupuuuupuculmgmqfvnbgtapekouga
* */

}
//leetcode submit region end(Prohibit modification and deletion)

}
// 最多删除一个字符得到回文
//给定一个非空字符串 s，请判断如果 最多 从字符串中删除一个字符能否得到一个回文字符串。 
//
// 
//
// 示例 1: 
//
// 
//输入: s = "aba"
//输出: true
// 
//
// 示例 2: 
//
// 
//输入: s = "abca"
//输出: true
//解释: 可以删除 "c" 字符 或者 "b" 字符
// 
//
// 示例 3: 
//
// 
//输入: s = "abc"
//输出: false 
//
// 
//
// 提示: 
//
// 
// 1 <= s.length <= 10⁵ 
// s 由小写英文字母组成 
// 
//
// 
//
// 注意：本题与主站 680 题相同： https://leetcode-cn.com/problems/valid-palindrome-ii/ 
// Related Topics 贪心 双指针 字符串 👍 39 👎 0
