package test._0526;

import java.sql.*;

public class dbConn {
    private final static String classname = "com.mysql.jdbc.Driver";
    private final static String dbStr = "jdbc:mysql://localhost:3306/test_mall";
    private final static String username = "bgzocg";
    private final static String password = "0";

    private Connection conn=null;

    public dbConn() throws ClassNotFoundException, SQLException{
        Class.forName(classname);
        conn = DriverManager.getConnection(dbStr, username, password);
    }

    public ResultSet exeSQL(String sql) throws SQLException{
        PreparedStatement preparedStatement;

        Statement st = conn.createStatement();
        ResultSet rs = st.executeQuery(sql);
        return rs;
    }
    public int exeUpdate(String sql) throws SQLException{
        Statement st = conn.createStatement();
        int row = st.executeUpdate(sql);
        return row;
    }
}