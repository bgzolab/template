<%--
  Created by IntelliJ IDEA.
  User: 15517
  Date: 5/26/2022
  Time: 10:14
  To change this template use File | Settings | File Templates.
--%>

<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>

<!DOCTYPE html>
<html>
<head>
    <title>Welcome Shopping System</title>
    <link rel="stylesheet" href="asserts/css/styles.css">
</head>
<body>

<div>
    <h1>Welcome Shopping System</h1>
</div>

<div>
    <form method="get" action="query.jsp">
        Money You Have: <input type="text" name="price" value="100"><br>
<%--        Tags You Want: <input type="text" name="tags" value="java"><br>--%>
        <input type="submit" value="Search">
    </form>
</div>

</body>
</html>