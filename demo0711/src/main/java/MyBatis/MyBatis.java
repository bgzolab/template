package MyBatis;

import JDBC.Student;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.InputStream;

/* File Name: MyBatis
 * Author: bGZo
 * Created Time: 7/12/2022 20:31
 * License: MIT
 * Description:
 */
public class MyBatis {
    public static void main(String[] args) throws IOException {
        String resource = "mybatis-config.xml";
        InputStream inputStream = Resources.getResourceAsStream(resource);

        SqlSessionFactoryBuilder sfb = new SqlSessionFactoryBuilder();
        SqlSessionFactory sqlSessionFactory = sfb.build(inputStream);
        SqlSession sqlSession = sqlSessionFactory.openSession();

        Student s =  new Student("20220714", "lihua", 20, 80.5, "2022");

        StudentMapperComment st =sqlSession.getMapper(StudentMapperComment.class);

        st.queryCount();
        sqlSession.commit();
        sqlSession.close();

    }
}
