<%-- 
    Document   : login
    Created on : 2022-5-9, 9:15:36
    Author     : david
--%>

<%@page import="com.mydb.DbConn"%>
<%@page import="java.sql.*"%>
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
            String username = request.getParameter("username");
            String password = request.getParameter("password");
            String sex = request.getParameter("sex");
            String[] fav = request.getParameterValues("fav");
            System.out.println("username=" + username);
            out.print("username=" + username);
            String favs="";
            for(int i=0;i<fav.length;i++)
                favs+=fav[i]+",";
            
            Connection conn;
            try {
            // TODO code application logic here
            //Class.forName("org.gjt.mm.mysql.Driver");旧的驱动类

            //Class.forName("com.mysql.jdbc.Driver");
            //mysql8用 Class.forName("com.mysql.cj.jdbc.Driver");
            //conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/test", "root", "root");
            //jdbc:mysql://localhost:3306/(数据库名)?useSSL=false&useUnicode=true&characterEncoding=UTF8&serverTimezone=GMT
            //mysql8用 DriverManager.getConnection("jdbc:mysql://localhost:3306/test?useSSL=false&useUnicode=true&characterEncoding=UTF8&serverTimezone=GMT", "root", "root");
            
            DbConn dbconn = new DbConn();
            
            //String upsql = "update product set price=? where productid=?";
            //PreparedStatement ps = conn.prepareStatement(upsql);
            //ps.setString(1, price);
            //ps.setString(2, pid);
            //int row1 = ps.executeUpdate();
            //String upsql = "update product set price=" + price + " where productid='" +  pid + "'";
            //System.out.println("upsql=" + upsql);
            
            //Statement st = conn.createStatement();
            //int row = st.executeUpdate(upsql);
                    
            String sql = "select * from myusers where username='" + username + "' and password='" + password + "'";
            System.out.println("sql=" +sql);
            //ResultSet rs = st.executeQuery(sql);
            ResultSet rs = dbconn.exeSQL(sql);
            if(rs.next()){
                /*
                System.out.print("id=" + rs.getString("productid"));
                System.out.print("\tname=" + rs.getString("proname"));
                System.out.print("\tprice=" + rs.getString("price"));
                System.out.println(); 
                */
                //out.print("登录成功！");
                //response.sendRedirect("index.html");
                session.setAttribute("user", username);
                %>
                <jsp:forward page="index.html"/>
                <%
            }else{
                //out.print("登录失败！");
                //response.sendRedirect("loginfail.jsp");  
                %>
                <jsp:forward page="loginfail.jsp"/>
                <%
            }
        } catch (Exception ex) {
            System.out.println("出错了" + ex.toString()); 
        } 
        
        %>
        用户名=<%="是"+username%>
        密码=<%=password%>
        性别=<%=sex%>
        爱好=<%=favs%>
    </body>
</html>
