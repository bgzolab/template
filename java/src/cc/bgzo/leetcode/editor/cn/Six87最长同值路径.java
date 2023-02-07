package cc.bgzo.leetcode.editor.cn;

import sun.reflect.generics.tree.Tree;

public class Six87最长同值路径{

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
        Solution solution = new Six87最长同值路径().new Solution();
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
    int depth = 0;
//    void traverse(TreeNode root, int max){
//        if(root == null) return;
//
//        int left=0;
//
//        if(root.left!=null){
//            if(root.left.val == root.val){
//                if(max+1 > depth){
//                    depth = max+1;
//                    left = depth;
//                }
//
//                traverse(root.left, max+1);
//            } else traverse(root.left, 0);
//        }
//
//        if(root.right!=null){
//            if(root.right.val == root.val){
//
//                if(left + max + 1 > depth){
//                    depth = left + max+1;
//                }
//                traverse(root.right, max+1);
//            } else traverse(root.right, 0);
//        }
//
//
//    }

//    void traverse(TreeNode root, int max) {
//        // 应该是自底向上算
//        if(root == null) return;
//
//        traverse(root.left);
//        traverse(root.right);
//    }

    int traverse(TreeNode root) {
        // 应该是自底向上算
        if(root == null) return 0;

        int left = traverse(root.left), right = traverse(root.right);
        int left1 = 0, right1 = 0;

        if( root.left!=null && root.left.val == root.val ){
            left1 = left + 1;
        }
        if( root.right!=null && root.right.val == root.val ){
            right1 = right + 1;
        }

        depth = Math.max(depth, left1 + right1);
        return Math.max(left1, right1);
    }

    public int longestUnivaluePath(TreeNode root) {
        traverse(root);
        return depth;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 最长同值路径
//给定一个二叉树的 root ，返回 最长的路径的长度 ，这个路径中的 每个节点具有相同值 。 这条路径可以经过也可以不经过根节点。 
//
// 两个节点之间的路径长度 由它们之间的边数表示。 
//
// 
//
// 示例 1: 
//
// 
//
// 
//输入：root = [5,4,5,1,1,5]
//输出：2
// 
//
// 示例 2: 
//
// 
//
// 
//输入：root = [1,4,5,4,4,5]
//输出：2
// 
//
// 
//
// 提示: 
//
// 
// 树的节点数的范围是 [0, 10⁴] 
// -1000 <= Node.val <= 1000 
// 树的深度将不超过 1000 
// 
// Related Topics 树 深度优先搜索 二叉树 👍 707 👎 0
