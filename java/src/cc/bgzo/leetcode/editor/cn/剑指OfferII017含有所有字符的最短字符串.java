package cc.bgzo.leetcode.editor.cn;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class 剑指OfferII017含有所有字符的最短字符串{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII017含有所有字符的最短字符串().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public String minWindow(String s, String t) {
        HashMap<Character, Integer> need= new HashMap<Character, Integer>();
        HashMap<Character, Integer> windows= new HashMap<Character, Integer>();

        int len1 = t.length();
        int ansl=0, ansr=0, min=Integer.MAX_VALUE;
        for(int i=0;i<len1; i++){
            Character ch = t.charAt(i);
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

            while(vaild == need.size()){
                if( min > right - left){
//                    ans.add(left);
                    min = right - left;
                    ansl = left;
                    ansr = right;
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
        return s.substring(ansl, ansr);
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 含有所有字符的最短字符串
//给定两个字符串 s 和 t 。返回 s 中包含 t 的所有字符的最短子字符串。如果 s 中不存在符合条件的子字符串，则返回空字符串 "" 。 
//
// 如果 s 中存在多个符合条件的子字符串，返回任意一个。 
//
// 
//
// 注意： 对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。 
//
// 
//
// 示例 1： 
//
// 
//输入：s = "ADOBECODEBANC", t = "ABC"
//输出："BANC" 
//解释：最短子字符串 "BANC" 包含了字符串 t 的所有字符 'A'、'B'、'C' 
//
// 示例 2： 
//
// 
//输入：s = "a", t = "a"
//输出："a"
// 
//
// 示例 3： 
//
// 
//输入：s = "a", t = "aa"
//输出：""
//解释：t 中两个字符 'a' 均应包含在 s 的子串中，因此没有符合条件的子字符串，返回空字符串。 
//
// 
//
// 提示： 
//
// 
// 1 <= s.length, t.length <= 10⁵ 
// s 和 t 由英文字母组成 
// 
//
// 
//
// 进阶：你能设计一个在 o(n) 时间内解决此问题的算法吗？ 
//
// 
//
// 注意：本题与主站 76 题相似（本题答案不唯一）：https://leetcode-cn.com/problems/minimum-window-
//substring/ 
// Related Topics 哈希表 字符串 滑动窗口 👍 50 👎 0
