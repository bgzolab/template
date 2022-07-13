package cc.bgzo.leetcode.editor.cn;
public class Six47回文子串{
    public static void main(String[] args) {
        Solution solution = new Six47回文子串().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {

        public int countSubstrings(String s) {
//    中心拓展
//        int len=s.length(), ans=0;
//        for(int i=0; i<len; i++){
//            ans+=count(s, i, i);
//            ans+=count(s, i, i+1);
//        }
//        return ans;
//    }
//
//    int count(String s, int i, int j){
//
//        int ans=0, len=s.length();
//        while(i>=0 && j<len){
//            if(s.charAt(i)!=s.charAt(j)) break;
//            i--;
//            j++;
//            ans++;
//        }
//        return ans;
//    }

//      Manacher 算法
            int n = s.length();
            StringBuffer t = new StringBuffer("$#");
            for (int i = 0; i < n; ++i) {
                t.append(s.charAt(i));
                t.append('#');
            }
            n = t.length();
            t.append('!');

            int[] f = new int[n];
            int iMax = 0, rMax = 0, ans = 0;
            for (int i = 1; i < n; ++i) {
                // 初始化 f[i]
                f[i] = i <= rMax ? Math.min(rMax - i + 1, f[2 * iMax - i]) : 1;
                // 中心拓展
                while (t.charAt(i + f[i]) == t.charAt(i - f[i])) {
                    ++f[i];
                }
                // 动态维护 iMax 和 rMax
                if (i + f[i] - 1 > rMax) {
                    iMax = i;
                    rMax = i + f[i] - 1;
                }
                // 统计答案, 当前贡献为 (f[i] - 1) / 2 上取整
                ans += f[i] / 2;
            }

            return ans;
//        via: https://leetcode.cn/problems/palindromic-substrings/solution/hui-wen-zi-chuan-by-leetcode-solution/
        }
    }
//leetcode submit region end(Prohibit modification and deletion)

}
// 回文子串
//给你一个字符串 s ，请你统计并返回这个字符串中 回文子串 的数目。 
//
// 回文字符串 是正着读和倒过来读一样的字符串。 
//
// 子字符串 是字符串中的由连续字符组成的一个序列。 
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
// Related Topics 字符串 动态规划 👍 918 👎 0
