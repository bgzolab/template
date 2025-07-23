<%-- 
    Document   : bookquery
    Created on : 2022-5-16, 9:33:47
    Author     : david
--%>

<%@page import="java.sql.*"%>
<%@page import="com.mydb.DbConn"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <h1><%=session.getAttribute("user") %>Hello World!</h1>
        <%
            request.setCharacterEncoding("utf-8");
            String price = request.getParameter("price");

            String sql = "select * from book where price>" + price;
            DbConn dbconn = new DbConn();
            ResultSet rs = dbconn.exeSQL(sql);
            %>
            <table border="1">
                <tr><td>书号</td><td>书名</td><td>出版社</td><td>价格</td><td>操作</td><td>操作</td></tr>
            <%
                           
            while(rs.next()){
               String bookid = rs.getString("bookid");
               String price1 = rs.getString("price");
            %>

            <tr><td><%=bookid %></td><td><%=rs.getString("bookname")%></td><td><%=rs.getString("pub")%></td><td ><font color="red"><%=price1%></font></td>
                <td ><font color="red"><a href="bookdelete.jsp?bookid=<%=bookid%>">删除</a>
            <td ><font color="red"><a href="addtocart.jsp?bookid=<%=bookid%>&price=<%=price1%>">加入购物车</a></tr>
                <%
            }
        %>
            </table>
    </body>
</html>
