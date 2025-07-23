package cc.bgzo.x4advanced;

import java.util.*;

/* File Name: x21LinkedList
 * Author: bGZo
 * Created Time: 11/6/2022 22:08
 * License: MIT
 * Description: TODO: UnsupportedOperationException() Method
 */
public class x21LinkedList implements List {
    static class ListNode {
        public ListNode(ListNode prev, ListNode next, Object value) {
            this.prev = prev;
            this.next = next;
            this.value = value;
        }
        ListNode prev;
        ListNode next;
        Object value;
    }
    ListNode start = null;
    ListNode tail = null;

    int size = 0;

    @Override
    public int size() {
        return size;
    }

    @Override
    public boolean isEmpty() {
        return size==0;
    }

    @Override
    public boolean contains(Object o) {
        ListNode curr = start;

        while (curr != null) {
            if (Objects.equals(curr.value, o)) {
                return true;
            }
            curr = curr.next;

        }
        return false;
    }

    @Override
    public Iterator iterator() {
        throw new UnsupportedOperationException();
    }

    @Override
    public Object[] toArray() {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean add(Object o) {
        ListNode newNode = new ListNode(tail, null, o);
        if (start == null) {
            start = newNode;
        }

        if (tail != null) {
            tail.next = newNode;
        }

        tail = newNode;

        size++;
        return true;
    }

    @Override
    public boolean remove(Object o) {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean addAll(Collection collection) {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean addAll(int i, Collection collection) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void clear() {
        start = null;
        tail = null;
        size = 0;
    }

    @Override
    public Object get(int i) {
        if (i > size || i < 0) {
            throw new IndexOutOfBoundsException("out of bound " + size + " for " + i);
        }
        ListNode curr = start;
        for (int j = 0; j < i; j++) {
            curr = curr.next;
        }
        return curr.value;
    }

    @Override
    public Object set(int i, Object o) {
        throw new UnsupportedOperationException();
    }

    @Override
    public void add(int i, Object o) {
        throw new UnsupportedOperationException();
    }

    @Override
    public Object remove(int i) {
        throw new UnsupportedOperationException();
    }

    @Override
    public int indexOf(Object o) {
        throw new UnsupportedOperationException();
    }

    @Override
    public int lastIndexOf(Object o) {
        throw new UnsupportedOperationException();
    }

    @Override
    public ListIterator listIterator() {
        throw new UnsupportedOperationException();
    }

    @Override
    public ListIterator listIterator(int i) {
        throw new UnsupportedOperationException();
    }

    @Override
    public List subList(int i, int i1) {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean retainAll(Collection collection) {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean removeAll(Collection collection) {
        throw new UnsupportedOperationException();
    }

    @Override
    public boolean containsAll(Collection collection) {
        throw new UnsupportedOperationException();

    }

    @Override
    public Object[] toArray(Object[] objects) {
        throw new UnsupportedOperationException();
    }
}
