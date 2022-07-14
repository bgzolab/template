#leetcode submit region begin(Prohibit modification and deletion)
# Write your MySQL query statement below

select users.user_id as buyer_id, join_date, ifnull(userbuy.cnt, 0) as orders_in_2019
from users left join (
    select buyer_id, count(order_id) cnt from orders
    where order_date between "2019-01-01" and "2019-12-31"
    group by buyer_id
    ) userbuy on users.user_id = userbuy.buyer_id;

#leetcode submit region end(Prohibit modification and deletion)

# 市场分析 I
#Table: Users 
#
# 
#+----------------+---------+
#| Column Name    | Type    |
#+----------------+---------+
#| user_id        | int     |
#| join_date      | date    |
#| favorite_brand | varchar |
#+----------------+---------+
#此表主键是 user_id。
#表中描述了购物网站的用户信息，用户可以在此网站上进行商品买卖。
# 
#
# 
#
# Table: Orders 
#
# 
#+---------------+---------+
#| Column Name   | Type    |
#+---------------+---------+
#| order_id      | int     |
#| order_date    | date    |
#| item_id       | int     |
#| buyer_id      | int     |
#| seller_id     | int     |
#+---------------+---------+
#此表主键是 order_id。
#外键是 item_id 和（buyer_id，seller_id）。
# 
#
# 
#
# Table: Items 
#
# 
#+---------------+---------+
#| Column Name   | Type    |
#+---------------+---------+
#| item_id       | int     |
#| item_brand    | varchar |
#+---------------+---------+
#此表主键是 item_id。
# 
#
# 
#
# 请写出一条SQL语句以查询每个用户的注册日期和在 2019 年作为买家的订单总数。 
#
# 以 任意顺序 返回结果表。 
#
# 查询结果格式如下。 
#
# 
#
# 示例 1: 
#
# 
#输入：
#Users 表:
#+---------+------------+----------------+
#| user_id | join_date  | favorite_brand |
#+---------+------------+----------------+
#| 1       | 2018-01-01 | Lenovo         |
#| 2       | 2018-02-09 | Samsung        |
#| 3       | 2018-01-19 | LG             |
#| 4       | 2018-05-21 | HP             |
#+---------+------------+----------------+
#Orders 表:
#+----------+------------+---------+----------+-----------+
#| order_id | order_date | item_id | buyer_id | seller_id |
#+----------+------------+---------+----------+-----------+
#| 1        | 2019-08-01 | 4       | 1        | 2         |
#| 2        | 2018-08-02 | 2       | 1        | 3         |
#| 3        | 2019-08-03 | 3       | 2        | 3         |
#| 4        | 2018-08-04 | 1       | 4        | 2         |
#| 5        | 2018-08-04 | 1       | 3        | 4         |
#| 6        | 2019-08-05 | 2       | 2        | 4         |
#+----------+------------+---------+----------+-----------+
#Items 表:
#+---------+------------+
#| item_id | item_brand |
#+---------+------------+
#| 1       | Samsung    |
#| 2       | Lenovo     |
#| 3       | LG         |
#| 4       | HP         |
#+---------+------------+
#输出：
#+-----------+------------+----------------+
#| buyer_id  | join_date  | orders_in_2019 |
#+-----------+------------+----------------+
#| 1         | 2018-01-01 | 1              |
#| 2         | 2018-02-09 | 2              |
#| 3         | 2018-01-19 | 0              |
#| 4         | 2018-05-21 | 0              |
#+-----------+------------+----------------+ 
# Related Topics 数据库 👍 49 👎 0
