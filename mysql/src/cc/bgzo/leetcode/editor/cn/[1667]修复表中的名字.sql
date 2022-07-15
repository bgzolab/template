#leetcode submit region begin(Prohibit modification and deletion)
# Write your MySQL query statement below

select user_id , (concat(upper(left(name, 1)), lower(substr(name, 2)))) name from users
order by user_id;

#leetcode submit region end(Prohibit modification and deletion)

# 修复表中的名字
#表： Users 
#
# 
#+----------------+---------+
#| Column Name    | Type    |
#+----------------+---------+
#| user_id        | int     |
#| name           | varchar |
#+----------------+---------+
#user_id 是该表的主键。
#该表包含用户的 ID 和名字。名字仅由小写和大写字符组成。
# 
#
# 
#
# 编写一个 SQL 查询来修复名字，使得只有第一个字符是大写的，其余都是小写的。 
#
# 返回按 user_id 排序的结果表。 
#
# 查询结果格式示例如下。 
#
# 
#
# 示例 1： 
#
# 
#输入：
#Users table:
#+---------+-------+
#| user_id | name  |
#+---------+-------+
#| 1       | aLice |
#| 2       | bOB   |
#+---------+-------+
#输出：
#+---------+-------+
#| user_id | name  |
#+---------+-------+
#| 1       | Alice |
#| 2       | Bob   |
#+---------+-------+ 
# Related Topics 数据库 👍 31 👎 0
