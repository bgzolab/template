#leetcode submit region begin(Prohibit modification and deletion)
# Write your MySQL query statement below

select distinct p1.email from Person p1, Person p2
where p1.id!=p2.id and p1.email=p2.email;

#leetcode submit region end(Prohibit modification and deletion)

# 查找重复的电子邮箱
#编写一个 SQL 查询，查找 Person 表中所有重复的电子邮箱。 
#
# 示例： 
#
# +----+---------+
#| Id | Email   |
#+----+---------+
#| 1  | a@b.com |
#| 2  | c@d.com |
#| 3  | a@b.com |
#+----+---------+
# 
#
# 根据以上输入，你的查询应返回以下结果： 
#
# +---------+
#| Email   |
#+---------+
#| a@b.com |
#+---------+
# 
#
# 说明：所有电子邮箱都是小写字母。 
# Related Topics 数据库 👍 374 👎 0
