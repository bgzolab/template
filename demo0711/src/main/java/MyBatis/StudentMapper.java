package MyBatis;

import JDBC.Student;

import java.util.List;

/* File Name: StudentMapper
 * Author: bGZo
 * Created Time: 7/12/2022 20:31
 * License: MIT
 * Description:
 */
public interface StudentMapper {
    public void saveStudent(Student s);
    public void removeStudent(Student id);
    public List<Student> queryList();
    public Student queryStudent(Student id);
    public Integer queryCount();
    public void updateStudent(Student st);
}
