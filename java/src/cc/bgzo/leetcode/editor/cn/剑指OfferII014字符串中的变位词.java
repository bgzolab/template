package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;

public class 剑指OfferII014字符串中的变位词{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII014字符串中的变位词().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public boolean checkInclusion(String s1, String s2) {
        HashMap<Character, Integer> need= new HashMap<Character, Integer>();
        HashMap<Character, Integer> windows= new HashMap<Character, Integer>();

        int len1 = s1.length();
        for(int i=0;i<len1; i++){
            Character ch = s1.charAt(i);
            need.put(ch, need.getOrDefault(ch, 0) + 1);
        }

        int left =0, right=0, vaild=0,
                len2 = s2.length();
        while (right < len2){
            Character ch = s2.charAt(right);
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
                if(vaild == need.size())
                    return true;

//                System.out.print(", vaild "+vaild);
//                System.out.print(",right "+ch);
                ch = s2.charAt(left);
                left++;
//                System.out.println(",left "+ch);

                if(need.containsKey(ch)){
                    if(windows.get(ch).equals(need.get(ch)))
                        vaild--;
                    windows.put(ch, windows.get(ch)-1);
                }
            }
        }
        return false;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 字符串中的变位词
//给定两个字符串 s1 和 s2，写一个函数来判断 s2 是否包含 s1 的某个变位词。 
//
// 换句话说，第一个字符串的排列之一是第二个字符串的 子串 。 
//
// 
//
// 示例 1： 
//
// 
//输入: s1 = "ab" s2 = "eidbaooo"
//输出: True
//解释: s2 包含 s1 的排列之一 ("ba").
// 
//
// 示例 2： 
//
// 
//输入: s1= "ab" s2 = "eidboaoo"
//输出: False
// 
//
// 
//
// 提示： 
//
// 
// 1 <= s1.length, s2.length <= 10⁴ 
// s1 和 s2 仅包含小写字母 
// 
//
// 
//
// 注意：本题与主站 567 题相同： https://leetcode-cn.com/problems/permutation-in-string/ 
// Related Topics 哈希表 双指针 字符串 滑动窗口 👍 52 👎 0
