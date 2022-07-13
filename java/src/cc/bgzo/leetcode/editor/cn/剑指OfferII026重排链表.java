package cc.bgzo.leetcode.editor.cn;

import org.w3c.dom.NodeList;

import java.util.ArrayList;
import java.util.List;

public class 剑指OfferII026重排链表{
    public class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII026重排链表().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public void reorderList(ListNode head) {
//        1. 线性表
//        if(head == null) return;
//        List<ListNode> list = new ArrayList<>();
//        ListNode node = head;
//        while(node!=null){
//            list.add(node);
//            node=node.next;
//        }
//
//        int i=0, j=list.size()-1;
//        while(i<j){
//            list.get(i).next = list.get(j);
//            i++;
//            list.get(j).next = list.get(i);
//            j--;
//        }
//        list.get(i).next = null;

//    2. 中点, 逆序, 合并


        char c=74;

    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 重排链表
//给定一个单链表 L 的头节点 head ，单链表 L 表示为： 
//
// L0 → L1 → … → Ln-1 → Ln 
//请将其重新排列后变为： 
//
// L0 → Ln → L1 → Ln-1 → L2 → Ln-2 → … 
//
// 不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。 
//
// 
//
// 示例 1: 
//
// 
//
// 
//输入: head = [1,2,3,4]
//输出: [1,4,2,3] 
//
// 示例 2: 
//
// 
//
// 
//输入: head = [1,2,3,4,5]
//输出: [1,5,2,4,3] 
//
// 
//
// 提示： 
//
// 
// 链表的长度范围为 [1, 5 * 10⁴] 
// 1 <= node.val <= 1000 
// 
//
// 
//
// 注意：本题与主站 143 题相同：https://leetcode-cn.com/problems/reorder-list/ 
// Related Topics 栈 递归 链表 双指针 👍 64 👎 0
