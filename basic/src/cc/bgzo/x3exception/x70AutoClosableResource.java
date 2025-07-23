package cc.bgzo.x3exception;

import java.io.IOException;

/* File Name: x70AutoClosableResource
 * Author: bGZo
 * Created Time: 11/6/2022 20:48
 * License: MIT
 * Description:
 */
public class x70AutoClosableResource implements AutoCloseable{
    private String resName;
    private int counter;

    public x70AutoClosableResource(String resName) {
        this.resName = resName;
    }

    public String read() throws IOException {
        counter++;
        if (Math.random() > 0.1) {
            return "You got lucky to read from " + resName + " for " + counter + " times...";
        } else {
            throw new IOException("resource不存在哦");
        }
    }
    @Override
    public void close() throws Exception {
        System.out.println("资源释放了:" + resName);
    }

    public static void main(String[] args) {
        try (
                x70AutoClosableResource res1 = new x70AutoClosableResource("res1");
                x70AutoClosableResource res2 = new x70AutoClosableResource("res2")
        ) {
            while (true) {
                System.out.println(res1.read());
                System.out.println(res2.read());
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
