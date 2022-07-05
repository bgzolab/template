package cc.bgzo.leetcode.editor.cn;

import java.util.HashMap;
import java.util.Map;

public class 剑指OfferII005{
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII005().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class Solution {
    public int maxProduct(String[] words) {
        Map<Integer, Integer> hm = new HashMap<>();
//        消除异构单词, 如 met & meet, 只记录不同的掩码值, 只需要更新最大单词长度就可以
//        int []mask = new int[words.length];

        for(int i = 0; i<words.length; i++){
            String str = words[i];
            int len = str.length(), mask = 0;
            for(int j=0; j<len; j++){
                mask |= 1 << (str.charAt(j)-'a');
//                mask[i] |= 1 << (str.charAt(j)-'a');
            }

            if(len > hm.getOrDefault(mask, 0)){
                hm.put(mask, len);
            }
        }


        int max = 0;
//        for(int i = 0; i<words.length; i++){
//            for(int j = i + 1; j<words.length; j++){
//                if((mask[i] & mask[j]) == 0){
//                    max = Math.max(max, words[i].length()*words[j].length());
//                }
//            }
//        }
        for(Integer mark1: hm.keySet()){
            for(Integer mark2: hm.keySet()) {
                if( (mark1 & mark2) ==0){
                    max = Math.max(max, hm.get(mark1)*hm.get(mark2));
                }
            }
        }// 空间使用要更友好一些
        return max;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 单词长度的最大乘积
//给定一个字符串数组 words，请计算当两个字符串 words[i] 和 words[j] 不包含相同字符时，它们长度的乘积的最大值。假设字符串中只包含英语
//的小写字母。如果没有不包含相同字符的一对字符串，返回 0。 
//
// 
//
// 示例 1: 
//
// 
//输入: words = ["abcw","baz","foo","bar","fxyz","abcdef"]
//输出: 16 
//解释: 这两个单词为 "abcw", "fxyz"。它们不包含相同字符，且长度的乘积最大。 
//
// 示例 2: 
//
// 
//输入: words = ["a","ab","abc","d","cd","bcd","abcd"]
//输出: 4 
//解释: 这两个单词为 "ab", "cd"。 
//
// 示例 3: 
//
// 
//输入: words = ["a","aa","aaa","aaaa"]
//输出: 0 
//解释: 不存在这样的两个单词。
// 
//
// 
//
// 提示： 
//
// 
// 2 <= words.length <= 1000 
// 1 <= words[i].length <= 1000 
// words[i] 仅包含小写字母 
// 
//
// 
//
// 注意：本题与主站 318 题相同：https://leetcode-cn.com/problems/maximum-product-of-word-lengths/
// Related Topics 位运算 数组 字符串 👍 86 👎 0
