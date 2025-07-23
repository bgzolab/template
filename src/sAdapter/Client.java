package sAdapter;

/* File Name: Client
 * Author: bGZo
 * Created Time: 6/23/2022 15:03
 * License: MIT
 * Description:
 */
public class Client {
    public static void main(String[] args) {
        // error or add (TriplePin) for: TriplePin triplePinDevice = new TV();

        DualPin dualPinDevice = new TV();

        // 1. 对象适配器
        // TriplePin triplePinDevice = new Adapter(dualPinDevice);
        // triplePinDevice.electrify(1, 0,-1);

        // 2. 类适配器
        TriplePin tvAvadpter = new TVAdapter();
        tvAvadpter.electrify(1, 0, -1);
    }
}
