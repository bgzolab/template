package cc.bgzo.leetcode.editor.cn;

import java.util.ArrayDeque;
import java.util.Deque;

public class 剑指OfferII025链表中的两数相加{
    public class ListNode {
        int val;
        ListNode next;
        ListNode() {}
        ListNode(int val) { this.val = val; }
        ListNode(int val, ListNode next) { this.val = val; this.next = next; }
    }
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII025链表中的两数相加().new Solution();
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
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
//        1. stack
//        Deque<Integer> s1 = new ArrayDeque<>();
//        Deque<Integer> s2 = new ArrayDeque<>();
//
//        while(l1!=null){
//            s1.push(l1.val);
//            l1=l1.next;
//        }
//        while(l2!=null){
//            s2.push(l2.val);
//            l2=l2.next;
//        }
//
//        int carry =0;
//        ListNode ans = null;
//        while (!s1.isEmpty() || !s2.isEmpty() || carry !=0){
//            int a = s1.isEmpty()? 0: s1.pop(),
//            b = s2.isEmpty()? 0: s2.pop(),
//            cur = a+b+carry;
//
//            carry = cur/10;
//            cur %= 10;
//            ListNode curnode = new ListNode(cur);
//            curnode.next = ans;
//            ans = curnode;
//        }
//        return ans;


        // 2. reverse nodelist + order add.
        l1 = reverseList(l1);
        l2 = reverseList(l2);

        int carry=0;
        ListNode ans = null;

        while ( l1!=null || l2!=null || carry!=0){
            int a, b, cur;
            if(l1!=null){ // NOTE: NOT l1.next
                a = l1.val;
                l1 = l1.next;
            }else {
                a=0;
            }
            if(l2!=null){ // NOTE: NOT l2.next
                b = l2.val;
                l2 = l2.next;
            }else {
                b=0;
            }

            cur = a+b+carry;
            carry = cur/10;
            cur %=10;
            ListNode newNode = new ListNode(cur);
            newNode.next=ans;
            ans=newNode;


        }

        return ans;
    }
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
// 链表中的两数相加
//给定两个 非空链表 l1和 l2 来代表两个非负整数。数字最高位位于链表开始位置。它们的每个节点只存储一位数字。将这两数相加会返回一个新的链表。 
//
// 可以假设除了数字 0 之外，这两个数字都不会以零开头。 
//
// 
//
// 示例1： 
//
// 
//
// 
//输入：l1 = [7,2,4,3], l2 = [5,6,4]
//输出：[7,8,0,7]
// 
//
// 示例2： 
//
// 
//输入：l1 = [2,4,3], l2 = [5,6,4]
//输出：[8,0,7]
// 
//
// 示例3： 
//
// 
//输入：l1 = [0], l2 = [0]
//输出：[0]
// 
//
// 
//
// 提示： 
//
// 
// 链表的长度范围为 [1, 100] 
// 0 <= node.val <= 9 
// 输入数据保证链表代表的数字无前导 0 
// 
//
// 
//
// 进阶：如果输入链表不能修改该如何处理？换句话说，不能对列表中的节点进行翻转。 
//
// 
//
// 注意：本题与主站 445 题相同：https://leetcode-cn.com/problems/add-two-numbers-ii/ 
// Related Topics 栈 链表 数学 👍 58 👎 0
