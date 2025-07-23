package cc.bgzo.x3exception;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/* File Name: x10TryCatch
 * Author: bGZo
 * Created Time: 11/6/2022 11:57
 * License: MIT
 * Description: 运行时异常
    * NOTE: try 语句中如果发生了异常（Exception），那么程序会跳转到catch语句。
    * NOTE: Java会将异常相关信息封装在一个异常类的实例中，ex是指向这个异常实例的引用
    * NOTE: "处理" 最简单的方法，就是调用printStackTrace将异常信息输出到控制台
    * NOTE: catch语句执行完毕，程序会继续向下顺序执行
 */

public class x10TryCatch {
    // x10ArrayIndexOutOfBoundsException
    public static void main(String[] args) {
        String []array ={
                "Hello World!"
        };
        String string = "";

        try{
            System.out.println(array[1]);
        } catch(ArrayIndexOutOfBoundsException e){
            e.printStackTrace();
        }

        try {
            string.substring(9, 10);
        } catch (Exception e) {
            e.printStackTrace();
        }

        System.out.println("Normal ended.");
    }
}

class TestListOfNumber {
    private ArrayList list;
    private static final int size = 10;

    public TestListOfNumber() {
        list = new ArrayList(size);
        for (int i = 0; i < size; i++)
            list.add(new Integer(i));
    }

    public void writeList() {
        PrintWriter out = null;

        try {
            System.out.println("Entering try statement");
            out = new PrintWriter(new FileWriter("outfile"));

            for (int i = 0; i < size; i++) {
                out.println("Value at: " + i + " = " + list.get(i));
            }
        } catch (ArrayIndexOutOfBoundsException e) { // 数组越界异常
            System.err.println(
                    "Caught ArrayIndexOutOfBoundsException: " +
                    e.getMessage());
        } catch (IOException e) {  // I/O异常
            System.err.println(
                    "Caught IOException: " +
                            e.getMessage());
        } finally {  // 最后清理
            if (out != null) {
                System.out.println("Closing PrintWriter");
                out.close();
            } else {
                System.out.println("PrintWriter not open");
            }
        }
    }
    public static void main(String[] args) {
        TestListOfNumber list = new TestListOfNumber();
        list.writeList();
    }
}
