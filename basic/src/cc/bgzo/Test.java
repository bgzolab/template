package cc.bgzo;
//import sun.security.util.ArrayUtil;
import java.io.*;

import java.lang.annotation.Annotation;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.net.URL;
import java.util.*;
@SuppressWarnings(value="unchecked")
@Deprecated
public class Test {
    // 为该类定义一个私有的构造器
    private Test(){}
    // 定义一个有参数的构造器
    public Test(String name){
        System.out.println("执行有参数的构造器");
    }
    // 定义一个无参数的info方法
    public void info(){
        System.out.println("执行无参数的info方法");
    }
    // 定义一个有参数的info方法
    public void info(String str){
        System.out.println("执行有参数的info方法"
                + "，其str参数值：" + str);
    }
    // 定义一个测试用的内部类
    class Inner{ }
    public static void main(String[] args)
            throws Exception{
        // 下面代码可以获取Test对应的Class
        Class<Test> clazz=Test.class;
        // 获取该Class对象所对应类的全部构造器
        Constructor[] ctors=clazz.getDeclaredConstructors();
        System.out.println("Test的全部构造器如下：");
        for (Constructor c : ctors){
            System.out.println(c);
        }
        // 获取该Class对象所对应类的全部public构造器
        Constructor[] publicCtors=clazz.getConstructors();
        System.out.println("Test的全部public构造器如下：");
        for (Constructor c : publicCtors){
            System.out.println(c);
        }
        // 获取该Class对象所对应类的全部public方法
        Method[] mtds=clazz.getMethods();
        System.out.println("Test的全部public方法如下：");
        for (Method md : mtds){
            System.out.println(md);
        }
        // 获取该Class对象所对应类的指定方法
        System.out.println("Test里带一个字符串参数的info方法为："
                + clazz.getMethod("info" , String.class));
        // 获取该Class对象所对应类的全部注释
        Annotation[] anns=clazz.getAnnotations();
        System.out.println("Test的全部Annotation如下：");
        for (Annotation an : anns){
            System.out.println(an);
        }
        System.out.println("该Class元素上的@SuppressWarnings注释为："
                + clazz.getAnnotation(SuppressWarnings.class));
        // 获取该Class对象所对应类的全部内部类
        Class<?>[] inners=clazz.getDeclaredClasses();
        System.out.println("Test的全部内部类如下：");
        for (Class c : inners){
            System.out.println(c);
        }
        // 使用Class.forName()方法加载Test的Inner内部类
        Class inClazz=Class.forName("cc.bgzo.Test$Inner");
//         通过getDeclaringClass()访问该类所在的外部类
        System.out.println("inClazz对应类的外部类为：" +
                inClazz.getDeclaringClass());
        System.out.println("Test的包为：" + clazz.getPackage());
        System.out.println("Test的父类为：" + clazz.getSuperclass());
    }
}



