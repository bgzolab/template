
select
    count()

from Activity

order by player_id

# Write an SQL query that reports the fraction of players that
# logged in again on the day after the day they first logged in,
# rounded to 2 decimal places. In other words, you need to count
# the number of players that logged in for at least two consecutive
# days starting from their first login date, then divide that number
# by the total number of players.
#
# 编写一个SQL查询，报告在首次登录的第二天再次登录的玩家的比率，
# 四舍五入到小数点后两位。换句话说，您需要计算从首次登录日期开始
# 至少连续两天登录的玩家的数量，然后除以玩家总数。
# The query result format is in the following example:
#
# Activity table:
# +-----------+-----------+------------+--------------+
# | player_id | device_id | event_date | games_played |
# +-----------+-----------+------------+--------------+
# | 1         | 2         | 2016-03-01 | 5            |
# | 1         | 2         | 2016-03-02 | 6            |
# | 2         | 3         | 2017-06-25 | 1            |
# | 3         | 1         | 2016-03-02 | 0            |
# | 3         | 4         | 2018-07-03 | 5            |
# +-----------+-----------+------------+--------------+
# Result table:
# +-----------+
# | fraction  |
# +-----------+
# | 0.33      |
# +-----------+
# Only the player with id 1 logged back in after the first day he had logged in so the answer is 1/3 = 0.33