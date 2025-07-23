package cc.bgzo.x4advanced;

import java.util.*;

/* File Name: x20ArrayList
 * Author: bGZo
 * Created Time: 11/6/2022 21:46
 * License: MIT
 * Description: TODO: UnsupportedOperationException() Method
 */
public class x20ArrayList implements List {

    Object[] elements;
    int curr;

    public x20ArrayList() {
        elements = new Object[16];
        curr = 0;
    }

    @Override
    public int size() {
        return curr;
    }

    @Override
    public boolean isEmpty() {
        return curr == 0;
    }

    @Override
    public boolean contains(Object o) {
        for(Object ele: elements){
            if(Objects.equals(ele, o)){
                return true;
            }
        }
        return false;
    }

    @Override
    public Iterator iterator() {
        throw new UnsupportedOperationException();
    }

    @Override
    public Object[] toArray() {
        return new Object[0];
    }

    @Override
    public boolean add(Object o) {
        if (curr == elements.length - 1) {
            Object[] temp = new Object[elements.length * 2];
            System.arraycopy(elements, 0, temp, 0, elements.length);
            elements = temp;
        }
        elements[curr] = o;
        curr++;
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
        curr = 0;
    }

    @Override
    public Object get(int i) {
        if(i > curr || i < 0){
            throw new IndexOutOfBoundsException("out of bound " + curr + " for "+ i);
        }
        return elements[i];
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
