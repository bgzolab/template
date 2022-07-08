package cc.bgzo.leetcode.editor.cn;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class 剑指OfferII015字符串中的所有变位词{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII015字符串中的所有变位词().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        HashMap<Character, Integer> need= new HashMap<Character, Integer>();
        HashMap<Character, Integer> windows= new HashMap<Character, Integer>();

        int len1 = p.length();
        List<Integer> ans = new ArrayList<>();
        for(int i=0;i<len1; i++){
            Character ch = p.charAt(i);
            need.put(ch, need.getOrDefault(ch, 0) + 1);
        }

        int left =0, right=0, vaild=0,
                len2 = s.length();
        while (right < len2){
            Character ch = s.charAt(right);
            right++;

            if(need.containsKey(ch)) {
//                这里先后顺序注意一下, 先push进去数据, 然后比较:
//                System.out.println("need contains" + ch);
//                System.out.print("need.get(ch) "+need.get(ch) + ", windows.getOrDefault(ch, 0)"+ windows.getOrDefault(ch, 0));
                windows.put(ch, windows.getOrDefault(ch, 0)+1);

                if(need.get(ch).equals(windows.getOrDefault(ch, 0)))
                    vaild++;
            }

            while(right - left >= len1){
                if(vaild == need.size()){
                    ans.add(left);
                }

//                System.out.print(", vaild "+vaild);
//                System.out.print(",right "+ch);
                ch = s.charAt(left);
                left++;
//                System.out.println(",left "+ch);

                if(need.containsKey(ch)){
                    if(windows.get(ch).equals(need.get(ch)))
                        vaild--;
                    windows.put(ch, windows.get(ch)-1);
                }
            }
        }
        return  ans;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 字符串中的所有变位词
//给定两个字符串 s 和 p，找到 s 中所有 p 的 变位词 的子串，返回这些子串的起始索引。不考虑答案输出的顺序。 
//
// 变位词 指字母相同，但排列不同的字符串。 
//
// 
//
// 示例 1： 
//
// 
//输入: s = "cbaebabacd", p = "abc"
//输出: [0,6]
//解释:
//起始索引等于 0 的子串是 "cba", 它是 "abc" 的变位词。
//起始索引等于 6 的子串是 "bac", 它是 "abc" 的变位词。
// 
//
// 示例 2： 
//
// 
//输入: s = "abab", p = "ab"
//输出: [0,1,2]
//解释:
//起始索引等于 0 的子串是 "ab", 它是 "ab" 的变位词。
//起始索引等于 1 的子串是 "ba", 它是 "ab" 的变位词。
//起始索引等于 2 的子串是 "ab", 它是 "ab" 的变位词。
// 
//
// 
//
// 提示: 
//
// 
// 1 <= s.length, p.length <= 3 * 10⁴ 
// s 和 p 仅包含小写字母 
// 
//
// 
//
// 注意：本题与主站 438 题相同： https://leetcode-cn.com/problems/find-all-anagrams-in-a-
//string/ 
// Related Topics 哈希表 字符串 滑动窗口 👍 30 👎 0
