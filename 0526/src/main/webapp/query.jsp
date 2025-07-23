<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/26/2022
  Time: 10:14
  To change this template use File | Settings | File Templates.
--%>

<%@page import="java.sql.*"%>
<%@page import="test._0526.dbConn"%>
<%@ page import="java.util.HashMap" %>
<%@ page import="java.util.Set" %>
<%@ page import="java.util.Iterator" %>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>Query Result</title>
        <link rel="stylesheet" href="asserts/css/styles.css">
    </head>

    <body>

        <h1>Results are Following:</h1>
        <%
            request.setCharacterEncoding("utf-8");
            String price = request.getParameter("price");
            String sql = "select * from goods where price <" + price;
            dbConn dbconn = new dbConn();
            ResultSet rs = dbconn.exeSQL(sql);
            session.setAttribute("queryPrice", price);
            %>
            <table border="1">
                <tr>
                    <td>Id</td>
                    <td>Name</td>
                    <td>Prices</td>
                    <td>Actions</td>
                </tr>
            <%
            while(rs.next()){
               String id = rs.getString("id");
               String prices = rs.getString("price");
            %>

            <tr>
                <td><%=id %></td>
                <td><%=rs.getString("name")%></td>
                <td><font color="red"><%=prices%></font></td>
                <td><font color="green"><a href="add-to-cart.jsp?id=<%=id%>&price=<%=prices%>">Add to Carts</a></td>
            </tr>
                <%
            }
//            HashMap<String, ResultSet> hashmap;
//            if(session.getAttribute("resultSet")==null){
//                hashmap = new HashMap<>();
//
//                while(rs.next()){
//                    String id = rs.getString("id");
//                    hashmap.put(id, rs);
//                }
//
//                session.setAttribute("resultSet", hashmap);
//            }else{
//                hashmap = (HashMap<String, ResultSet>) session.getAttribute("resultSet");
//            }

        %></table>

        <h1>Cart are Following:</h1>
        <%

            HashMap hm = (HashMap)session.getAttribute("cart");
            if(hm==null) {
                out.print("Cart is Null!");
                out.print("<br>");
            }else{
                Set s = hm.keySet();
                Iterator it = s.iterator();

                out.print("<table border=\"1\">" +
                        "<tr>" +
                        "<td>Id</td>" +
                        "<td>Number</td>" +
                        "<td>Actions</td>\n");

                while(it.hasNext()){
                    String key = (String)it.next();
                    Integer num = (Integer)hm.get(key);
                    out.print(  "<tr>"+
                            "<td>" + key + "</td>" +
//                            "<td>" + hashmap.get(key).getString("name") + "</td>" +
                            "<td>" + num + "</td>" +
                            "<td><a href=\"delete-from-cart.jsp?id="+ key + "\">Delete</a></td>" +
                            "</tr>\n");

                }
                out.print("</table>");
            }
        %>
    </body>
</html>

<%--<td><font color="red"><a href="delete-from-cart.jsp?id=<%=id%>">delete</a></font></td>--%>
<%--            <a href="show-cart.jsp">Show Carts</a>--%>
