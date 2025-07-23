package cc.bgzo;

public class Person {
    //定义一个初始化块
    int a=9;
    int b=9;

    {
        a = 6;
    }

    //定义无参数的构造器
    public Person() {
        System.out.println("Person类的无参数构造器");
    }

    public static void main(String[] args) {
        System.out.println(new Person().a);
        System.out.println(new Person().b);

    }
}


class Root
{
    static{
        System.out.println("Root的静态初始化块");
    }
    {
        System.out.println("Root的普通初始化块");
    }
    public Root()
    {
        System.out.println("Root的无参数的构造器");
    }
}
class Mid extends Root
{
    static{
        System.out.println("Mid的静态初始化块");
    }
    {
        System.out.println("Mid的普通初始化块");
    }
    public Mid()
    {
        System.out.println("Mid的无参数的构造器");
    }
    public Mid(String msg)
    {
        //通过this调用同一类中重载的构造器
        this();
        System.out.println("Mid的带参数构造器，其参数值："
                + msg);
    }
}
class Leaf extends Mid
{
    static{
        System.out.println("Leaf的静态初始化块");
    }
    {
        System.out.println("Leaf的普通初始化块");
    }
    public Leaf()
    {
        //通过super调用父类中有一个字符串参数的构造器
        super("疯狂Java讲义");
        System.out.println("执行Leaf的构造器");
    }
}
