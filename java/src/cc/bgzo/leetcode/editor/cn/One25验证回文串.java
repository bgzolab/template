package cc.bgzo.leetcode.editor.cn;
public class One25验证回文串{
    public static void main(String[] args) {
        Solution solution = new One25验证回文串().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean isPalindrome(String s) {
        StringBuilder sb = new StringBuilder();
        int len=s.length();
        for(int i=0;i<len;i++){
            if(Character.isLetterOrDigit(s.charAt(i)))
                sb.append(Character.toLowerCase(s.charAt(i)));
        }
        int lo = 0, hi=sb.length()-1;

        while (lo<=hi){
            if(sb.charAt(lo)!=sb.charAt(hi)) return false;
            lo++;
            hi--;
        }
        return true;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 验证回文串
//给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。 
//
// 说明：本题中，我们将空字符串定义为有效的回文串。 
//
// 
//
// 示例 1: 
//
// 
//输入: "A man, a plan, a canal: Panama"
//输出: true
//解释："amanaplanacanalpanama" 是回文串
// 
//
// 示例 2: 
//
// 
//输入: "race a car"
//输出: false
//解释："raceacar" 不是回文串
// 
//
// 
//
// 提示： 
//
// 
// 1 <= s.length <= 2 * 10⁵ 
// 字符串 s 由 ASCII 字符组成 
// 
// Related Topics 双指针 字符串 👍 546 👎 0
