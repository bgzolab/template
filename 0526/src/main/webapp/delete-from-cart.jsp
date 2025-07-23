<%@ page import="test._0526.dbConn" %>
<%@ page import="java.sql.ResultSet" %>
<%@ page import="java.sql.SQLException" %>
<%@ page import="java.util.HashMap" %>
<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/28/2022
  Time: 12:38
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>Delete</title>
    <link rel="stylesheet" href="asserts/css/styles.css">
</head>
<body>
    <%
        request.setCharacterEncoding("utf-8");
        String id = request.getParameter("id");
        HashMap hm = (HashMap)session.getAttribute("cart");
        if(hm==null)
            out.print("Cart is Null.");
        else {
            Integer num = (Integer)hm.get(id);
            num--;
            hm.put(id, num);

            if(num <= 0)
                hm.remove(id);

            session.setAttribute("cart", hm);

            out.print("<h1>Remove Sucessful</h1>");
        }
    %>
    <a href="query.jsp?price=<%=session.getAttribute("queryPrice")%>">Back query</a>
</body>
</html>