<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/26/2022
  Time: 10:14
  To change this template use File | Settings | File Templates.
--%>

<%@page import="java.util.HashMap"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <title>Add to Carts</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="stylesheet" href="asserts/css/styles.css">
    </head>
    <body>
        <h1>Add Successful</h1>

        <%
            request.setCharacterEncoding("utf-8");
            String id = request.getParameter("id");

            HashMap hm = (HashMap)session.getAttribute("cart");
            if(hm==null)
                hm = new HashMap();
            Integer num = (Integer)hm.get(id);

            if(num==null)
                num=0;

            num++;

            hm.put(id, num);
            session.setAttribute("cart", hm);
        %>

        <a href="query.jsp?price=<%=session.getAttribute("queryPrice")%>">Back query</a>
    </body>
</html>