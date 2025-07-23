<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/26/2022
  Time: 10:14
  To change this template use File | Settings | File Templates.
--%>

<%@page import="java.util.*"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Show Carts</title>
        <link rel="stylesheet" href="css/styles.css">
    </head>
    <body>
        <h1>Your Carts are Following:</h1>
        <%

            HashMap hm = (HashMap)session.getAttribute("cart");
            if(hm==null) {
                out.print("Carts is Null!");
                out.print("<br>");
            }else{
                Set s = hm.keySet();
                Iterator it = s.iterator();

                out.print("<table border=\"1\">" +
                        "<tr>" +
                        "<td>Id</td>" +
                        "<td>Number</td>" +
                        "<td>Actions</td>" +
                        "<br>");

                while(it.hasNext()){
                    String key = (String)it.next();
                    Integer num = (Integer)hm.get(key);
                    out.print(  "<tr>"+
                                "<td>" + key + "</td>" +
                                "<td>" + num + "</td>" +
                                "<td><a href=\"delete-from-cart.jsp?id="+ key + "\">Delete</a></td>" +
                                "</tr><br>");
                }
                out.print("</table>");
            }

        %>
        <a href="../query.jsp?price=<%=session.getAttribute(">Back query</a>
    </body>
</html>
