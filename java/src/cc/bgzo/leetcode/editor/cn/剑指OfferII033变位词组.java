package cc.bgzo.leetcode.editor.cn;

import java.lang.reflect.Array;
import java.util.*;

public class 剑指OfferII033变位词组{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII033变位词组().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public List<List<String>> groupAnagrams(String[] strs) {

        // 1. sort
        Map<String, List<String>> mp = new HashMap<>();
        for(String str: strs){
            char[] ch = str.toCharArray();
            Arrays.sort(ch);
            String s = Arrays.toString(ch);
            if(!mp.containsKey(s)){
                mp.put(s, new ArrayList<>());
            }
            mp.get(s).add(str);
        }
        return new ArrayList<>(mp.values());

        //2.

    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 变位词组
//给定一个字符串数组 strs ，将 变位词 组合在一起。 可以按任意顺序返回结果列表。 
//
// 注意：若两个字符串中每个字符出现的次数都相同，则称它们互为变位词。 
//
// 
//
// 示例 1: 
//
// 
//输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
//输出: [["bat"],["nat","tan"],["ate","eat","tea"]] 
//
// 示例 2: 
//
// 
//输入: strs = [""]
//输出: [[""]]
// 
//
// 示例 3: 
//
// 
//输入: strs = ["a"]
//输出: [["a"]] 
//
// 
//
// 提示： 
//
// 
// 1 <= strs.length <= 10⁴ 
// 0 <= strs[i].length <= 100 
// strs[i] 仅包含小写字母 
// 
//
// 
//
// 注意：本题与主站 49 题相同： https://leetcode-cn.com/problems/group-anagrams/ 
// Related Topics 数组 哈希表 字符串 排序 👍 32 👎 0
