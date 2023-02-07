package cc.bgzo.leetcode.editor.cn;
public class One115交替打印FooBar{
    public static void main(String[] args) {
        FooBar solution = new One115交替打印FooBar().new FooBar(0);
    }
    //leetcode submit region begin(Prohibit modification and deletion)
class FooBar {
        /**
         * ERROR
         *  1. Thrown exception java.lang.IllegalMonitorStateException: current thread is not owner
         *  2. Time Limit Exceeded
         *
         * Ways
         *  1. BLOCKING Queue 阻塞队列
         *      BlockingQueue is a java Queue that support operations that wait for
         *      the queue to become non-empty when retrieving and removing an element,
         *      and wait for space to become available in the queue when adding an
         *      element.
         *      via: https://www.digitalocean.com/community/tutorials/java-blockingqueue-example
         *  2. CyclicBarrier 控制先后
         *  3. spinlock 自旋锁 + 让出CPU
         *  4. lock 可重入锁 + Condition
         *  5. synchronized + 标志位 + 唤醒
         *  6. Semaphore  信号量 适合控制顺序
         *
         *  Via: https://leetcode.cn/problems/print-foobar-alternately/comments/728464
         *  FIXME: 3个 或 3个以上 进行交替输出怎么做???
         *  
         */
    private int n;
    final Object foo = new Object();
    private volatile boolean type = true;

    public FooBar(int n) {
        this.n = n;
    }

    public void foo(Runnable printFoo) throws InterruptedException {
        
        for (int i = 0; i < n; i++) {
            synchronized (foo){
                while(!type){
                    foo.wait();
                }


                // printFoo.run() outputs "foo". Do not change or remove this line.
                printFoo.run();
                type=false;
                foo.notifyAll();
            }
        }
    }

    public void bar(Runnable printBar) throws InterruptedException {
        
        for (int i = 0; i < n; i++) {
            synchronized (foo){

                while(type){
                    foo.wait();
                }

                // printBar.run() outputs "bar". Do not change or remove this line.
                printBar.run();
                type=true;
                foo.notifyAll();
            }
        }
    }
}
//leetcode submit region end(Prohibit modification and deletion)

}


// 交替打印 FooBar
//给你一个类： 
//
// 
//class FooBar {
//  public void foo() {
//    for (int i = 0; i < n; i++) {
//      print("foo");
//    }
//  }
//
//  public void bar() {
//    for (int i = 0; i < n; i++) {
//      print("bar");
//    }
//  }
//}
// 
//
// 两个不同的线程将会共用一个 FooBar 实例： 
//
// 
// 线程 A 将会调用 foo() 方法，而 
// 线程 B 将会调用 bar() 方法 
// 
//
// 请设计修改程序，以确保 "foobar" 被输出 n 次。 
//
// 
//
// 示例 1： 
//
// 
//输入：n = 1
//输出："foobar"
//解释：这里有两个线程被异步启动。其中一个调用 foo() 方法, 另一个调用 bar() 方法，"foobar" 将被输出一次。
// 
//
// 示例 2： 
//
// 
//输入：n = 2
//输出："foobarfoobar"
//解释："foobar" 将被输出两次。
// 
//
// 
//
// 提示： 
//
// 
// 1 <= n <= 1000 
// 
// Related Topics 多线程 👍 168 👎 0

