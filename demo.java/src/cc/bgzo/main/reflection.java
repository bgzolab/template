package main;

import java.lang.reflect.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

/* File Name: reflection
 * Author: bGZo
 * Created Time: 7/16/2022 12:13
 * License: MIT
 * Description:
 */

//class Solution {
//    int swh(int i){
//        int sum=0;
//        while (i!=0){
//            sum += i%10;
//            i/=10;
//        }
//        return sum;
//    }
//
//    public int[] numberOfPairs(int[] nums) {
//        HashMap<Integer, Integer> hm = new HashMap<>();
//        for(int i : nums){
//            hm.put(i, hm.getOrDefault(i,0)+ 1);
//        }
//
//        int ans[] = new int[]{0,0};
//
//        for (Integer key : hm.keySet()) {
//            if(hm.get(key) == 1) {
//                ans[1]++;
//                continue;
//            }else{
//                ans[0] += hm.get(key)/2;
//                if(hm.get(key)%2 == 1) ans[1]++;
//            }
//        }
//
//        return ans;
//    }
//}

//        Arrays.sort(nums);
//        int ans[] = new int[]{0,0};
//
//        List<Integer> intList = new ArrayList<Integer>(nums.length);
//        for (int i : nums)
//            intList.add(i);
//
//        for(int i=1; i<intList.size(); i++){
//            if(intList.get(i) == intList.get(i-1)){
//                System.out.println(nums[i] + " not " + nums[i-1]);
//                intList.remove(i);
//                intList.remove(i-1);
//                ans[0]++;
//            }
//        }
//
//        for (int i : nums)
//            System.out.println(i);
//        ans[1]=intList.size();
//
//        return ans;
//        int lo=0, hi=0;
//
//        while(hi < nums.length){
//            hi++;
//            if( lo!=hi && nums[lo] != nums[hi] ){
//                ans[1]++;
//                lo++;
//                continue;
//            }
//            ans[0]++;
//            lo++;
//        }
//        System.out.println(ans[0]);
//        System.out.println(ans[1]);
//



public class reflection {
    public static void main(String[] args) throws Exception {
//        new reflection().dynamicProxyCode();
        InvocationHandler handler = new InvocationHandler() {
            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                System.out.println(method);
                if (method.getName().equals("morning")) {
                    System.out.println("Good morning, " + args[0]);
                }
                return null;
            }
        };
        // 定义一个 InvocationHandler 实例，负责实现接口的方法调用
        // 通过 Proxy.newProxyInstance() 创建 interface 实例，它需要 3 个参数：
        // 使用的 ClassLoader，通常就是接口类的 ClassLoader；
        // 需要实现的接口数组，至少需要传入一个接口进去；
        // 用来处理接口方法调用的InvocationHandler实例。
        // 将返回的Object强制转型为接口
        Hello hello = (Hello) Proxy.newProxyInstance(
                Hello.class.getClassLoader(), // 传入ClassLoader
                new Class[] { Hello.class }, // 传入要实现的接口
                handler); // 传入处理调用方法的InvocationHandler
        hello.morning("Bob");
    }
    public static void dynamicProxyCode(String[] args) {

    }


    interface Hello {
        void morning(String name);
    }
    /***/
    class HelloWorld implements Hello {
        public void morning(String name) {
            System.out.println("Good morning, " + name);
        }
    }
    public void staticCode(){
        Hello hello = new HelloWorld();
        hello.morning("Bob");
    }

    /***/
    public void upwardTransformation(){
        Object n = Integer.valueOf(123);
        boolean isDouble = n instanceof Double; // false
        boolean isInteger = n instanceof Integer; // true
        boolean isNumber = n instanceof Number; // true
        boolean isSerializable = n instanceof java.io.Serializable; // true

        // Integer i = ?
        Integer.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Integer
        // Number n = ?
        Number.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Number
        // Object o = ?
        Object.class.isAssignableFrom(Integer.class); // true，因为Integer可以赋值给Object
        // Integer i = ?
        Integer.class.isAssignableFrom(Number.class); // false，因为Number不能赋值给Integer
    }

    /***/
    public void getInterfaceParent() throws Exception {
        Class s = Integer.class.getSuperclass();
        Class[] is = s.getInterfaces();
        for (Class i : is) {
            System.out.println(i);
        }
        System.out.println(java.io.DataInputStream.class.getSuperclass());
        // java.io.FilterInputStream，因为DataInputStream继承自FilterInputStream
        System.out.println(java.io.Closeable.class.getSuperclass());
        // null，对接口调用getSuperclass()总是返回null，获取接口的父接口要用getInterfaces()
    }

    /***/
    public void getInterface() throws Exception {
        Class s = Integer.class;
        Class[] is = s.getInterfaces();
        for (Class i : is) {
            System.out.println(i);
        }
        /*
        *   java.lang.Comparable
            java.lang.constant.Constable
            java.lang.constant.ConstantDesc
        * */
    }

    /**/
    public void getParentClass() throws Exception {
        Class i = Integer.class;
        Class n = i.getSuperclass();
        System.out.println(n);
        Class o = n.getSuperclass();
        System.out.println(o);
        System.out.println(o.getSuperclass());
    }

    /**/
    public void invokeUnpublicMethod() throws Exception {
        Person p = new Person();
        Method m = p.getClass().getDeclaredMethod("setName", String.class);
        m.setAccessible(true);
        m.invoke(p, "Bob");
        System.out.println(p.name);
    }

    /**/
    public void invokeStaticMethod() throws Exception {
        // 获取Integer.parseInt(String)方法，参数为String:
        Method m = Integer.class.getMethod("parseInt", String.class);
        // 调用该静态方法并获取结果:
        Integer n  = (Integer) m.invoke(null, "12345");
        // 打印调用结果:
        System.out.println(n);
    }

    /**/
    public void invokeNormalMethod() throws Exception {
        // String对象:
        String s = "Hello world";
        // 获取String substring(int)方法，参数为int:
        Method m = String.class.getMethod("substring", int.class);
        // 在s对象上调用该方法并获取结果:
        String r = (String) m.invoke(s, 6);
        // 打印调用结果:
        System.out.println(r);
    }

    /***/
    public void setFildValue() throws Exception {
        Person p = new Person("Xiao Ming");
        System.out.println(p.getName()); // "Xiao Ming"
        Class c = p.getClass();
        Field f = c.getDeclaredField("name");
        f.setAccessible(true);
        f.set(p, "Xiao Hong");
        System.out.println(p.getName()); // "Xiao Hong"
    }

    /***/
    public void getFildValue() throws Exception {
        Object p = new Person("Xiao Ming");
        Class c = p.getClass();
        Field f = c.getDeclaredField("name");
        f.setAccessible(true); // NOTE: Or "IllegalAccessException"
        Object value = f.get(p);
        System.out.println(value); // "Xiao Ming"
    }

    /***/
    public static void getDeclaredFieldInfo() throws NoSuchFieldException {
        Field f = String.class.getDeclaredField("value");
        f.getName(); // "value"
        f.getType(); // class [B 表示byte[]类型
        int m = f.getModifiers();
        Modifier.isFinal(m); // true
        Modifier.isPublic(m); // false
        Modifier.isProtected(m); // false
        Modifier.isPrivate(m); // true
        Modifier.isStatic(m); // false
    }

    /***/
    public static void getStudentPersonInfo() throws Exception {
        Class stdClass = Student.class;
        // 获取public字段"score":
        System.out.println(stdClass.getField("score"));
        // 获取继承的public字段"name":
        System.out.println(stdClass.getField("name"));
        // 获取private字段"grade":
        System.out.println(stdClass.getDeclaredField("grade"));
    }

    class Student extends Person {
        public int score;
        private int grade;

        public Student(String name) {
            super(name);
        }
    }

    class Person {
        public String name;

        public Person() { }
        public Person(String name) {
            this.name = name;
        }
        public String getName() {
            return this.name;
        }
        private void setName(String name) {
            this.name = name;
        }
    }

    /***/
    public static void getClassInfo(String[] args) {
        printClassInfo("".getClass());
        printClassInfo(Runnable.class);
        printClassInfo(java.time.Month.class);
        printClassInfo(String[].class);
        printClassInfo(int.class);
    }

    static void printClassInfo(Class cls) {
        System.out.println("Class name: " + cls.getName());
        System.out.println("Simple name: " + cls.getSimpleName());
        if (cls.getPackage() != null) {
            System.out.println("Package name: " + cls.getPackage().getName());
        }
        System.out.println("is interface: " + cls.isInterface());
        System.out.println("is enum: " + cls.isEnum());
        System.out.println("is array: " + cls.isArray());
        System.out.println("is primitive: " + cls.isPrimitive());
        System.out.println("");

    }
}
