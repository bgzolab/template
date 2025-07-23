package sAdapter;

/* File Name: Adapter
 * Author: bGZo
 * Created Time: 6/23/2022 15:05
 * License: MIT
 * Description: 对象适配器, 区别于 TVAdapter
 */
public class Adapter implements TriplePin{

    private DualPin dualPinDevice;

    public Adapter(DualPin dualPinDevice){
        this.dualPinDevice = dualPinDevice;
    }

    @Override
    public void electrify(int l, int n, int e) {
        dualPinDevice.electrify(l , n);
    }
}
