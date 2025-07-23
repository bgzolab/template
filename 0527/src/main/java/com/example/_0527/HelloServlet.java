package com.example._0527;

import java.io.*;
import javax.servlet.http.*;
import javax.servlet.annotation.*;
import java.sql.*;


//@WebServlet(name = "helloServlet", value = "/hello-servlet")
public class HelloServlet extends HttpServlet {
//    private String message;
//
//    public void init() {
//        message = "Hello World!";
//    }
//
//    public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
//        response.setContentType("text/html");
//
//        // Hello
//        PrintWriter out = response.getWriter();
//        out.println("<html><body>");
//        out.println("<h1>" + message + "</h1>");
//        out.println("</body></html>");
//    }
//
//    public void destroy() {
//    }


    private final static String classname = "com.mysql.jdbc.Driver";
    private final static String dbStr = "jdbc:mysql://localhost:3306/test_mall";
    private final static String username = "bgzocg";
    private final static String password = "0";

    private Connection conn=null;

    public dbConn() throws ClassNotFoundException, SQLException{
        Class.forName(classname);
        //mysql8用 Class.forName("com.mysql.cj.jdbc.Driver");
        conn = DriverManager.getConnection(dbStr, username, password);
    }

    public ResultSet exeSQL(String sql) throws SQLException{
        Statement st = conn.createStatement();
        ResultSet rs = st.executeQuery(sql);
        return rs;
    }
    public int exeUpdate(String sql) throws SQLException{
        Statement st = conn.createStatement();
        int row = st.executeUpdate(sql);
        return row;
    }
}