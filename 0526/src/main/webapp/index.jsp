<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/26/2022
  Time: 10:14
  To change this template use File | Settings | File Templates.
--%>

<%@page import="test._0526.dbConn"%>
<%@page import="java.sql.*"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>JSP Page</title>
    <link rel="stylesheet" href="asserts/css/styles.css">

</head>

<body>
    <%i++;%>
    <%!int i=100;%>
    <%
        request.setCharacterEncoding("utf-8");
        String username = request.getParameter("username");
        String password = request.getParameter("password");

//        System.out.println("username=" + username);
//        out.print("username=" + username);

        Connection conn;
        try {
            dbConn dbconn = new dbConn();
            String sql =
                    "select * from users where username='" + username + "' and password='" + password + "'";
            ResultSet rs = dbconn.exeSQL(sql);
            if(rs.next()){
                session.setAttribute("users", username);
                response.sendRedirect("select-by-price.jsp");
            }else{
                response.sendRedirect("loginfail.jsp");
            }
        } catch (Exception ex) {
                System.out.println(ex.toString());
        }%>
    </body>
</html>
