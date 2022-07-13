package cc.bgzo.leetcode.editor.cn;
public class 剑指OfferII029排序的循环链表{
    class Node {
        public int val;
        public Node next;
        public Node() {}
        public Node(int _val) {val = _val;}
        public Node(int _val, Node _next) {
            val = _val;
            next = _next;
        }
    };
    public static void main(String[] args) {
        Solution solution = new 剑指OfferII029排序的循环链表().new Solution();
    }
    //leetcode submit region begin(Prohibit modification and deletion)
/*
// Definition for a Node.
class Node {
    public int val;
    public Node next;

    public Node() {}

    public Node(int _val) {
        val = _val;
    }

    public Node(int _val, Node _next) {
        val = _val;
        next = _next;
    }
};
*/

class Solution {
    public Node insert(Node head, int insertVal) {
//        if(head == null){
//            Node newNode = new Node(insertVal);
//            head = newNode;
//            newNode.next = newNode;
//        } else if(head.next == head){
////            Node newNode = new Node(insertVal);
////            newNode.next = head;
////            head.next = newNode;
//
//            head.next = new Node(insertVal);
//            head.next.next=head;
//        } else {
//            Node tmp =head, minNode=head, maxNode=head, pre=null;
//            do{
//                if(minNode.next.val > tmp.val){
//                    minNode = pre;
//                }
//
//                if(maxNode.val < tmp.val)
//                    maxNode=tmp;
//                pre = tmp;
//                tmp = tmp.next;
//            } while (tmp != head);
//
//            if(insertVal < minNode.next.val){
//                Node newNode = new Node(insertVal);
//                newNode.next = minNode.next;
//                minNode.next.next = newNode;
//            }
//
//            if(insertVal>maxNode.val){
//                Node newNode = new Node(insertVal);
//                newNode.next = maxNode.next;
//                maxNode.next = newNode;
//            }
//            NOTE: 插最大, 最小有问题.
//            tmp =head;
//            do{
//                if(tmp.val < insertVal)
//                    break;
//                tmp = tmp.next;
//            } while(tmp!=head);
//
//            Node cur = tmp;
//            pre = null;
//            while(true){ // cur!=head && pre!=head
////                System.out.println(pre.val+" 1"+cur.val);
//
//                if( cur.val >= insertVal && pre.val <= insertVal){
////                    System.out.println(pre.val+" "+cur.val);
//                    pre.next = new Node(insertVal);
//                    pre.next.next =  cur;
//                    break;
//                }
//                pre = cur;
//                cur = cur.next;
//            }
//        }


        Node node = new Node(insertVal);

        if(head==null){
            node.next = node;
            return node;
        }
        if(head.next == head){
            head.next = node;
            node.next =head;
            return head;
        }
        Node cur = head, next = head.next;

        while (next != head){
            if(insertVal >= cur.val && insertVal <= next.val)
                break;

            if(cur.val > next.val){
                if(insertVal > cur.val || insertVal < next.val){
                    break;
                }
            }
            cur = cur.next;
            next = next.next;
        }
        cur.next = node;
        node.next = next;
        return head;
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}
//// 排序的循环链表
////给定循环单调非递减列表中的一个点，写一个函数向这个列表中插入一个新元素 insertVal ，使这个列表仍然是循环升序的。
////
//// 给定的可以是这个列表中任意一个顶点的指针，并不一定是这个列表中最小元素的指针。
////
//// 如果有多个满足条件的插入位置，可以选择任意一个位置插入新的值，插入后整个列表仍然保持有序。
////
//// 如果列表为空（给定的节点是 null），需要创建一个循环有序列表并返回这个节点。否则。请返回原先给定的节点。
//
// 
//
// 示例 1： 
//
// 
// 
//
// 
//输入：head = [3,4,1], insertVal = 2
//输出：[3,4,1,2]
//解释：在上图中，有一个包含三个元素的循环有序列表，你获得值为 3 的节点的指针，我们需要向表中插入元素 2 。新插入的节点应该在 1 和 3 之间，插入之后
//，整个列表如上图所示，最后返回节点 3 。
//
//
// 
//
// 示例 2： 
//
// 
//输入：head = [], insertVal = 1
//输出：[1]
//解释：列表为空（给定的节点是 null），创建一个循环有序列表并返回这个节点。
// 
//
// 示例 3： 
//
// 
//输入：head = [1], insertVal = 0
//输出：[1,0]
// 
//
// 
//
// 提示： 
//
// 
// 0 <= Number of Nodes <= 5 * 10^4 
// -10^6 <= Node.val <= 10^6 
// -10^6 <= insertVal <= 10^6 
// 
//
// 
//
// 注意：本题与主站 708 题相同： https://leetcode-cn.com/problems/insert-into-a-sorted-
//circular-linked-list/ 
// Related Topics 链表 👍 112 👎 0
