package MyBatis;

import JDBC.Student;
import org.apache.ibatis.annotations.*;

import java.util.List;

/* File Name: StudentMapper
 * Author: bGZo
 * Created Time: 7/12/2022 20:31
 * License: MIT
 * Description:
 */
public interface StudentMapperComment {

    @Insert("insert into student values(#{id}, #{username}, #{age}, #{score},#{teacherId})")
    public void saveStudent(Student s);

    @Insert("<script> insert into student values\n" +
            "<foreach collection=\"list\" item=\"item\" separator=\",\">\n" +
            "{#{item.id},#{item.userName},#{item.age}, #{item.score}, #{item.teacherId}} .jhu </foreach></script>")
    public void saveStudent(List<Student> st);

    @Delete("delete from student where id=#{id}\n")
    public void removeStudent(Student id);

    @ResultMap("studentResult")
    @Select("select * from student")
    public List<Student> queryList();

    @Results(id="studentResult" , value = {
            @Result(property = "id", column = "id", id = true),
            @Result(property = "userName", column = "user_name"),
            @Result(property = "age", column = "age"),
            @Result(property = "score", column = "score"),
            @Result(property = "teacherId", column = "teacher_id")
    })
    @Select("select * from student where id=#{id}")
    public Student queryStudent(Student id);

    @Select("select count(*) from student where teacher_id=#{teacher_id}")
    public Integer queryCount();

    @Update("update student\n" +
            "<set>\n" +
            "<if test=\"userName!=null\">userName=#{userName}</if>\n" +
            "<if test=\"age!=null\"> age=#{age}</if>\n" +
            "<if test=\"score!=null\">score=#{score}</if>\n" +
            "<if test=\"teacher_id!=null\">teacher_id=#{teacherId}</if>\n" +
            "</set>\n" +
            "where id=#{id}")
    public void updateStudent(Student st);
}
