#leetcode submit region begin(Prohibit modification and deletion)
# Write your MySQL query statement below

select product_id from Products
where low_fats = "Y" and recyclable = "Y";

#leetcode submit region end(Prohibit modification and deletion)

# 可回收且低脂的产品
#表：Products 
#
# 
#+-------------+---------+
#| Column Name | Type    |
#+-------------+---------+
#| product_id  | int     |
#| low_fats    | enum    |
#| recyclable  | enum    |
#+-------------+---------+
#product_id 是这个表的主键。
#low_fats 是枚举类型，取值为以下两种 ('Y', 'N')，其中 'Y' 表示该产品是低脂产品，'N' 表示不是低脂产品。
#recyclable 是枚举类型，取值为以下两种 ('Y', 'N')，其中 'Y' 表示该产品可回收，而 'N' 表示不可回收。 
#
# 
#
# 写出 SQL 语句，查找既是低脂又是可回收的产品编号。 
#
# 返回结果 无顺序要求 。 
#
# 查询结果格式如下例所示： 
#
# 
#Products 表：
#+-------------+----------+------------+
#| product_id  | low_fats | recyclable |
#+-------------+----------+------------+
#| 0           | Y        | N          |
#| 1           | Y        | Y          |
#| 2           | N        | Y          |
#| 3           | Y        | Y          |
#| 4           | N        | N          |
#+-------------+----------+------------+
#Result 表：
#+-------------+
#| product_id  |
#+-------------+
#| 1           |
#| 3           |
#+-------------+
#只有产品 id 为 1 和 3 的产品，既是低脂又是可回收的产品。
# 
# Related Topics 数据库 👍 37 👎 0
