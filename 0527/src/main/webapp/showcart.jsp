<%-- 
    Document   : addtocart
    Created on : 2022-5-23, 8:44:09
    Author     : david
--%>

<%@page import="java.util.*"%>
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
            HashMap hm = (HashMap)session.getAttribute("cart");
            if(hm==null)
                out.print("购物车为空");
            else{
                Set s = hm.keySet();
                Iterator it = s.iterator();
                while(it.hasNext()){
                    String key = (String)it.next();
                    Integer num = (Integer)hm.get(key);
                    out.print("bookid=" + key + "  num=" + num + "<br>");
                }
            }
        %>
        <a href="showcart.jsp">显示购物车</a>
    </body>
</html>
