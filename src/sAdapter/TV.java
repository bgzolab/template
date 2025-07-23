package sAdapter;

/* File Name: TV
 * Author: bGZo
 * Created Time: 6/23/2022 15:03
 * License: MIT
 * Description:
 */
public class TV implements DualPin{
    @Override
    public void electrify(int l, int n) {
        System.out.println("火线通电：" + l + "，零线通电：" + n);
        System.out.println("电视开机");
    }
}
