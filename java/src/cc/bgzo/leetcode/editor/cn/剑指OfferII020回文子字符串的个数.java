package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII020回文子字符串的个数{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII020回文子字符串的个数().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    char[] chars;
    public int countSubstrings(String s) {
        int ans =0;
        chars = s.toCharArray();

        for(int i=0; i< chars.length; i++ ){
            ans +=count (i, i);
            ans +=count (i, i+1);
        }
        return ans;
    }

    public int count(int i, int j){
        int left = i-1, right = i+1, res=0;
        while ( i >= 0 && j < chars.length){
            if(chars[i--] ==  chars[j++]) res++;
            else break;
        }
        return res;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 回文子字符串的个数
//给定一个字符串 s ，请计算这个字符串中有多少个回文子字符串。 
//
// 具有不同开始位置或结束位置的子串，即使是由相同的字符组成，也会被视作不同的子串。 
//
// 
//
// 示例 1： 
//
// 
//输入：s = "abc"
//输出：3
//解释：三个回文子串: "a", "b", "c"
// 
//
// 示例 2： 
//
// 
//输入：s = "aaa"
//输出：6
//解释：6个回文子串: "a", "a", "a", "aa", "aa", "aaa" 
//
// 
//
// 提示： 
//
// 
// 1 <= s.length <= 1000 
// s 由小写英文字母组成 
// 
//
// 
//
// 注意：本题与主站 647 题相同：https://leetcode-cn.com/problems/palindromic-substrings/ 
// Related Topics 字符串 动态规划 👍 56 👎 0
