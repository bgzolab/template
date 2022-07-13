package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII024反转链表{
    public class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII024反转链表().new Solution();
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
    public ListNode reverseList(ListNode head) {


        if(head==null || head.next==null){//NOTE: NOT head.next==null || head.next.next==null
            return head;
        }

        ListNode newHead = reverseList(head.next);

        head.next.next=head;
        head.next=null;

        return newHead;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
// 反转链表
//给定单链表的头节点 head ，请反转链表，并返回反转后的链表的头节点。 
//
// 
// 
// 
//
// 示例 1： 
//
// 
//输入：head = [1,2,3,4,5]
//输出：[5,4,3,2,1]
// 
//
// 示例 2： 
//
// 
//输入：head = [1,2]
//输出：[2,1]
// 
//
// 示例 3： 
//
// 
//输入：head = []
//输出：[]
// 
//
// 
//
// 提示： 
//
// 
// 链表中节点的数目范围是 [0, 5000] 
// -5000 <= Node.val <= 5000 
// 
//
// 
//
// 进阶：链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？ 
// 
// 
//
// 
//
// 注意：本题与主站 206 题相同： https://leetcode-cn.com/problems/reverse-linked-list/ 
// Related Topics 递归 链表 👍 78 👎 0
