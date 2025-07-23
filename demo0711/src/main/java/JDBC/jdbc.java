package JDBC;

import java.sql.*;
//import com.mysql.jdbc.*;

/* File Name: jdbc
 * Author: bGZo
 * Created Time: 7/11/2022 15:33
 * License: MIT
 * Description:
 */

public class jdbc {
    public static void main(String[] args) throws SQLException, ClassNotFoundException, InstantiationException, IllegalAccessException {

        Class.forName("com.mysql.cj.jdbc.Driver");

        String sql = "select count(*) from goods";
        String url = "jdbc:mysql://127.0.0.1:3306/test_mall?useSSL=false";
        String user = "bgzocg";
        String password = "0";

        Connection connection = DriverManager.getConnection(url, user, password);

        PreparedStatement pre = connection.prepareStatement(sql);
        ResultSet res = pre.executeQuery();
        System.out.println(res.next());

    }

}
