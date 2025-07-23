- spring全家桶
  - spring
  - springmvc
  - spring boot
  - spring cloud
- 核心技术
  - ioc, Inversion of Control
    - 控制反转, 一个理论, 概念, 思想
    - 描述的
      - 把对象的创建，赋值，管理工作都交给代码之外的容器实现， 也就是对象的创建是有其它外部资源完成
    - 控制
      - 创建对象，对象的属性赋值，对象之间的关系管理
    - 反转
      - 把管理, 创建对象, 给属性赋值的权限转移给代码之外的容器实现
      - 由容器代替开发人员
      - 正转
        - 开发人员 new 主动构造方法
      - 容器
        - 一个服务器软件， 一个框架 (spring)
    - 例子: servlet
      - 创建类继承 HttpServelt 
      - 在 web.xml 注册servlet
        ```xml
        <servlet-name> myservlet </servlet-name>
        <servelt-class>com.bjpwernode.controller.MyServlet1</servlet-class>
        ```
      - 没有主动创建 Servlet对象.
      - Servlet 是Tomcat服务器它能你创建的。 Tomcat也称为容器, Tomcat作为容器：里面存放的有Servlet对象， Listener ， Filter对象
    - 技术实现 -- DI, Dependency Injection
      - 只需要在程序中提供要使用的对象名称就可以, 至于对象如何在容器中创建, 赋值，查找都由容器内部实现
      - spring底层创建对象，使用的是反射机制。
      - spring是一个容器，管理对象，给属性赋值， 底层是反射创建对象
      - 基于注解的 di
        - 使用步骤
          - 加入maven的依赖 `spring-context`
            - 在你加入spring-context的同时， 间接加入spring-aop的依赖。使用注解必须使用spring-aop依赖
          - 类中加入spring的注解 (多个不同功能的注解)
          - 在spring的配置文件中，加入一个组件扫描器的标签，说明注解在你的项目中的位置
      - 重要的注解
        - `@Component`
        - `@Respotory`
        - `@Service`
        - `@Controller`
        - `@Value`
        - `@Autowired`
        - `@Resource`
  - aop, Aspect Orient Programming, 面向切面编程
    - 基于动态代理
      - 实现方式
        - jdk动态代理
          - 使用jdk中的Proxy，Method，InvocaitonHanderl创建代理对象。
            - jdk动态代理要求目标类必须实现接口
        - cglib动态代理
          - 第三方的工具库，创建代理对象，原理是继承。 通过继承目标类，创建子类。
          - 子类就是代理对象。 要求目标类不能是final的， 方法也不能是final的
      - 作用
        - 在目标类源代码不改变的情况下，增加功能。
        - 减少代码的重复
        - 专注业务逻辑代码
        - 解耦合，让你的业务功能和日志，事务非业务功能分离。
    - 理解切面
      - 特点
        - 一般都是非业务方法，独立使用的
      - 需要在分析项目功能时，找出切面。
      - 合理的安排切面的执行时间（在目标方法前， 还是目标方法后）
      - 合理的安全切面执行的位置，在哪个类，哪个方法增加增强功能
    - 术语
      - Aspect
        - 切面，表示增强的功能， 就是一堆代码，完成某个一个功能。非业务功能，
          - 常见的切面功能有日志， 事务， 统计信息， 参数检查， 权限验证。
      - JoinPoint
        - 连接点 ，连接业务方法和切面的位置。 就某类中的业务方法
      - Pointcut
        - 切入点 ，指多个连接点方法的集合。多个方法
      - 目标对象
        - 给哪个类的方法增加功能， 这个类就是目标对象
      - Advice
        - 通知，通知表示切面功能执行的时间
    - 三要素
      - 切面的功能代码，切面干什么
      - 切面的执行位置，使用Pointcut表示切面执行的位置
      - 切面的执行时间，使用Advice表示时间，在目标方法之前，还是目标方法之后。
    - 实现
      - spring
        - 内部实现了 aop 规范
        - 主要在事务处理时使用 aop
          - 较笨重
      - aspectJ
        - 一个开源的专门做aop的框架。spring框架中集成了aspectj框架，通过spring就能使用aspectj的功能。
        - aspectJ框架实现aop有两种方式：
          - 使用xml的配置文件
            - 配置全局事务
          - 使用注解, aspectj有5个注解
            - 切面的执行时间， 这个执行时间在规范中叫做Advice(通知，增强)
            - 在aspectj框架中使用注解表示的。也可以使用xml配置文件中的标签
              - @Before
              - @AfterReturning
              - @Around
              - @AfterThrowing
              - @After
            - 表示切面执行的位置，使用的是切入点表达式
              ```java
              com.service.impl
              com.bjpowrnode.service.impl
              cn.crm.bjpowernode.service
              
              execution(* *..service.*.*(..))
              ```

- mybatis + spring
  - 技术 Stack
    - IoC
      - ioc能创建对象, 可以把mybatis框架中的对象交给spring统一创建， 开发人员从spring中获取对象。开发人员就不用同时面对两个或多个框架了， 就面对一个spring
  - 使用步骤
    - 定义 `dao` 接口 `StudentDao`
    - 定义 `mapper` 文件 `StudentDao.xml`
    - 定义 `mybatis` 的主配置文件 `mybatis.xml`
    - 创建 `dao` 的代理对象 
      - `StudentDao dao = SqlSession.getMapper(StudentDao.class);`
      - `List<Student> students  = dao.selectStudents();`
  - 连接池
    - 多个连接Connection对象的集合
      ```java
      List<Connection>  connlist; // connList就是连接池
      
      // 通常使用Connection访问数据库
      Connection conn =DriverManger.getConnection(url,username,password);
      Statemenet stmt = conn.createStatement(sql);
      stmt.executeQuery();
      conn.close();
      ```



要使用dao对象，需要使用getMapper()方法，怎么能使用getMapper()方法，需要哪些条件
1.获取SqlSession对象， 需要使用SqlSessionFactory的openSession()方法。
2.创建SqlSessionFactory对象。 通过读取mybatis的主配置文件，能创建SqlSessionFactory对象

需要SqlSessionFactory对象， 使用Factory能获取SqlSession ，有了SqlSession就能有dao ， 目的就是获取dao对象
Factory创建需要读取主配置文件

我们会使用独立的连接池类替换mybatis默认自己带的， 把连接池类也交给spring创建。


- 事务处理
  - 事务
    - mysql 
      - 指一组sql语句的集合, 集合中有多条sql语句
      - 可能是insert ， update ，select ，delete， 我们希望这些多个sql语句都能成功，或者都失败， 这些sql语句的执行是一致的，作为一个整体执行
  - 什么时候用事务
    - 涉及得到多个表，或者是多个sql语句的insert，update，delete。需要保证这些语句都是成功才能完成我的功能，或者都失败，保证操作是符合要求的
  - 事务架构
    - 应该放在 service 类的业务方法上，因为业务方法会调用多个dao方法，执行多个sql语句
  - 使用流程
    ```java
    // jdbc
    Connection conn;
    conn.commit();
    conn.rollback();
    
    // mybatis
    SqlSession.commit();
    SqlSession.rollback();

    // hibernate
    Session.commit();
    Session.rollback();
    ```
    - 不足: 多种数据库的访问技术，有不同的事务处理的机制，对象，方法。
      - 不同的数据库访问技术，处理事务的对象，方法不同，需要了解不同数据库访问技术使用事务的原理
      - 掌握多种数据库中事务的处理逻辑。什么时候提交事务，什么时候回顾事务
      - 处理事务的多种方法
      - 解决方案
        - spring的事务处理机制
        - 
  - ......


- web 项目中使用容器对象
  - 需求
    - web项目中容器对象只需要创建一次, 把容器对象放入到全局作用域ServletContext中
    - 实现
      - 监听器
        - 当全局作用域对象被创建时 创建容器 存入ServletContext
        - 作用
          - 创建容器对象，执行 `ApplicationContext ctx = new ClassPathXmlApplicationContext("applicationContext.xml");`
          - 把容器对象放入到`ServletContext， ServletContext.setAttribute(key,ctx)`
        - 可以自己创建，也可以使用框架中提供好的ContextLoaderListener
        - `ApplicationContext`: Javase
        - `WebApplicationContext`: Web












=========================================
- java中创建对象有哪些方式：
  - 构造方法
    - `new Student()`
  - 反射
  - 序列化
  - 克隆
  - ioc
    - 容器创建对象
  - 动态代理
=========================================
- 用户处理请求：
  - 用户form (参数name, age)
    - Servlet (接收请求name, age)
      - Service类 (处理name, age操作)
        - dao类(访问数据库的)
          - mysql
=========================================
