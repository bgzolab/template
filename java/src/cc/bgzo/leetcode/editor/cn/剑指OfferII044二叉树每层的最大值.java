package cc.bgzo.leetcode.editor.cn;

import sun.reflect.generics.tree.Tree;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public class 剑指OfferII044二叉树每层的最大值{
    public class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode() {}
        TreeNode(int val) { this.val = val; }
        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII044二叉树每层的最大值().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    public List<Integer> largestValues(TreeNode root) {

        if(root == null){
            return new ArrayList<>();
        }

        Queue<TreeNode> queue = new ArrayDeque<>();
        queue.offer(root);

        List<Integer> ans = new ArrayList<>();

        while(!queue.isEmpty()){
            int max = Integer.MIN_VALUE,
            len = queue.size();

            /**
             * NOTE: 怎么区别不同层的边界?
             * 具体实现参照 len
             * 不同于「广搜」每次只从队列里拿出一个节点，我们把当前队列中的全部节点拿出来进行拓展，
             * 这样能保证每次拓展完的时候队列里存放的是下一层的所有节点，
             * 即我们是一层一层地进行拓展，然后每一层我们用 maxVal 来标记该层节点的最大值
             *
             * via: https://leetcode.cn/problems/hPov7L/solution/er-cha-shu-mei-ceng-de-zui-da-zhi-by-lee-q4y2/
             */

            while(len > 0){
                len--;
                TreeNode node = queue.poll();
                max = Math.max(max, node.val);
                if(node.left!=null) queue.offer(node.left);
                if(node.right!=null) queue.offer(node.right);
            }
            ans.add(max);

        }
        return ans;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 二叉树每层的最大值
//给定一棵二叉树的根节点 root ，请找出该二叉树中每一层的最大值。 
//
// 
//
// 示例1： 
//
// 
//输入: root = [1,3,2,5,3,null,9]
//输出: [1,3,9]
//解释:
//          1
//         / \
//        3   2
//       / \   \  
//      5   3   9 
// 
//
// 示例2： 
//
// 
//输入: root = [1,2,3]
//输出: [1,3]
//解释:
//          1
//         / \
//        2   3
// 
//
// 示例3： 
//
// 
//输入: root = [1]
//输出: [1]
// 
//
// 示例4： 
//
// 
//输入: root = [1,null,2]
//输出: [1,2]
//解释:      
//           1 
//            \
//             2     
// 
//
// 示例5： 
//
// 
//输入: root = []
//输出: []
// 
//
// 
//
// 提示： 
//
// 
// 二叉树的节点个数的范围是 [0,10⁴] 
// -2³¹ <= Node.val <= 2³¹ - 1 
// 
//
// 
//
// 注意：本题与主站 515 题相同： https://leetcode-cn.com/problems/find-largest-value-in-
//each-tree-row/ 
// Related Topics 树 深度优先搜索 广度优先搜索 二叉树 👍 29 👎 0
