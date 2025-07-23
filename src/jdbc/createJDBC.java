package jdbc;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/* File Name: testJDBC
 * Author: @bGZo
 * Created Time: 5/8/2022 16:35
 * License: MIT
 * Description:
 */
public class testJDBC {

    public static void main(String[] args) {
        try {
            //1.注册驱动
            Class.forName("com.mysql.cj.jdbc.Driver" );

        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }

        Connection conn = null;
        Statement statement = null;
        //2.建立连接并创建数据库和表
        try {
            conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/", "bgzocg", "0");
            statement = conn.createStatement();

            String sql1="drop database if exists mysql_db";
            String sql2="create database mysql_db";
            statement.executeUpdate(sql1);//执行sql语句
            statement.executeUpdate(sql2);

        } catch (SQLException e) {
            e.printStackTrace();
        }

        try {
            statement.executeUpdate("use mysql_db");//选择在哪个数据库中操作
            String sql = "create table student(" +
                    "id int not null, " +
                    "name varchar(20), " +
                    "sex varchar(4), " +
                    "age int" +
                    ")";
            statement.executeUpdate(sql);
        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if(statement!=null)
                    statement.close();
                if(conn!=null)
                    conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }

    }
}
