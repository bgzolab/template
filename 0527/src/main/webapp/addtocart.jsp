<%-- 
    Document   : addtocart
    Created on : 2022-5-23, 8:44:09
    Author     : david
--%>

<%@page import="java.util.HashMap"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <h1>Hello World!</h1>
        <%
            request.setCharacterEncoding("utf-8");
            String bookid = request.getParameter("bookid");
            //String price = request.getParameter("price");
            
            HashMap hm = (HashMap)session.getAttribute("cart");
            if(hm==null)
                hm = new HashMap();
            Integer num = (Integer)hm.get(bookid);
            if(num==null)
                num=0;
            num++;
            hm.put(bookid, num);
            session.setAttribute("cart",hm );
            
        %>
        <a href="showcart.jsp">显示购物车</a>
    </body>
</html>
