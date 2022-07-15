#leetcode submit region begin(Prohibit modification and deletion)
# Write your MySQL query statement below

select employee_id, (
    case when MOD(employee_id, 2)!=0 and LEFT(name,1)!='M' then salary
        else 0 end ) bonus from employees order by employee_id;


#leetcode submit region end(Prohibit modification and deletion)

# 计算特殊奖金
#表: Employees 
#
# 
#+-------------+---------+
#| 列名        | 类型     |
#+-------------+---------+
#| employee_id | int     |
#| name        | varchar |
#| salary      | int     |
#+-------------+---------+
#employee_id 是这个表的主键。
#此表的每一行给出了雇员id ，名字和薪水。
# 
#
# 
#
# 写出一个SQL 查询语句，计算每个雇员的奖金。如果一个雇员的id是奇数并且他的名字不是以'M'开头，那么他的奖金是他工资的100%，否则奖金为0。 
#
# Return the result table ordered by employee_id. 
#
# 返回的结果集请按照employee_id排序。 
#
# 查询结果格式如下面的例子所示。 
#
# 
#
# 示例 1: 
#
# 
#输入：
#Employees 表:
#+-------------+---------+--------+
#| employee_id | name    | salary |
#+-------------+---------+--------+
#| 2           | Meir    | 3000   |
#| 3           | Michael | 3800   |
#| 7           | Addilyn | 7400   |
#| 8           | Juan    | 6100   |
#| 9           | Kannon  | 7700   |
#+-------------+---------+--------+
#输出：
#+-------------+-------+
#| employee_id | bonus |
#+-------------+-------+
#| 2           | 0     |
#| 3           | 0     |
#| 7           | 7400  |
#| 8           | 0     |
#| 9           | 7700  |
#+-------------+-------+
#解释：
#因为雇员id是偶数，所以雇员id 是2和8的两个雇员得到的奖金是0。
#雇员id为3的因为他的名字以'M'开头，所以，奖金是0。
#其他的雇员得到了百分之百的奖金。 
# Related Topics 数据库 👍 54 👎 0
