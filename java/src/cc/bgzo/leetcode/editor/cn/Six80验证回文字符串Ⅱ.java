package cc.bgzo.leetcode.editor.cn;
public class Six80验证回文字符串Ⅱ{
    public static void main(String[] args) {
        Solution solution = new Six80验证回文字符串Ⅱ().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean validPalindrome(String s) {

        int lo =0 , hi =s.length()-1;

        while(lo<=hi){
            if(s.charAt(lo)!=s.charAt(hi)){
                break;
            }
            lo++;hi--;
        }
        if(lo>=hi) return true;
        return isPalindrome(s, lo)||isPalindrome(s,hi);
    }
    boolean isPalindrome(String s, int index){

        int lo =0 , hi =s.length()-1;
        while(lo<=hi){
            if(lo==index) lo++;
            if(hi==index) hi--;
            // NOTE: notice skip location !!!

            if(s.charAt(lo)!=s.charAt(hi)){
                return false;
            }
            lo++;hi--;

        }
        return true;
    }

}
//leetcode submit region end(Prohibit modification and deletion)

}
// 验证回文字符串 Ⅱ
//给定一个非空字符串 s，最多删除一个字符。判断是否能成为回文字符串。 
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
//解释: 你可以删除c字符。
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
// Related Topics 贪心 双指针 字符串 👍 513 👎 0
