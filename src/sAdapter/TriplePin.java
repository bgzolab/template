package sAdapter;

/* File Name: TriplePin
 * Author: bGZo
 * Created Time: 6/23/2022 15:00
 * License: MIT
 * Description:
 */
public interface TriplePin {
    /* 火线(live), 零线(null) 和 地线(earth) */
    public void electrify(int l, int n, int e);
}
