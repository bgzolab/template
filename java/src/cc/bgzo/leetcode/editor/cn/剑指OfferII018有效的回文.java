package cc.bgzo.leetcode.editor.cn;

import java.net.StandardSocketOptions;

public class 剑指OfferII018有效的回文{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII018有效的回文().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean isPalindrome(String s) {
//        int len = s.length();
//        String str = "";
//        for(int i=0;i<len;i++){
//            if(Character.isAlphabetic(s.charAt(i)) || Character.isDigit(s.charAt(i))){
//                str+=Character.toLowerCase(s.charAt(i));
//            }
//        }
//
//        int len2 = str.length(), left = 0, right = len2-1;
//
//        if(str=="")return true;
//
//        while(left<=right){
//            if(str.charAt(left)!=str.charAt(right)) return false;
//            left++;
//            right--;
//        }
//        return true;


        StringBuffer sgood = new StringBuffer();
        int len = s.length();

        for(int i=0;i<len;i++){
            char ch= s.charAt(i);
//            if(Character.isAlphabetic(ch) || Character.isDigit(ch)){
            if(Character.isLetterOrDigit(ch)){
                sgood.append(Character.toLowerCase(ch));
            }
        }

        int left = 0, right = sgood.length()-1;

        while(left<=right){
            if(sgood.charAt(left)!=sgood.charAt(right)) return false;
            left++;
            right--;
        }
        return true;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 有效的回文
//给定一个字符串 s ，验证 s 是否是 回文串 ，只考虑字母和数字字符，可以忽略字母的大小写。 
//
// 本题中，将空字符串定义为有效的 回文串 。 
//
// 
//
// 示例 1: 
//
// 
//输入: s = "A man, a plan, a canal: Panama"
//输出: true
//解释："amanaplanacanalpanama" 是回文串 
//
// 示例 2: 
//
// 
//输入: s = "race a car"
//输出: false
//解释："raceacar" 不是回文串 
//
// 
//
// 提示： 
//
// 
// 1 <= s.length <= 2 * 10⁵ 
// 字符串 s 由 ASCII 字符组成 
// 
//
// 
//
// 注意：本题与主站 125 题相同： https://leetcode-cn.com/problems/valid-palindrome/ 
// Related Topics 双指针 字符串 👍 25 👎 0
