-- Window function
select
       player_id,
       event_date,
       sum(games_played) over (partition by player_id order by event_date)
        -- only could use after express, not column
from Activity

-- Self Join??
select
            a.player_id,
            a.event_date,
            sum(b.games_played) as games_played_so_far
from
            Activity a join Activity b
on
            a.player_id = b.player_id
where
            a.event_date >= b.event_date
group by
            a.player_id, a.event_date
order by
            a.player_id;


# 编写一个SQL查询，同时报告每组玩家和日期，以及玩家到目前为止玩了多少游戏。
# 也就是说，在此日期之前玩家所玩的游戏总数。详细情况请查看示例
# 查询结果格式如下所示：
# Activity table:
# +--------------+---------+
# | Column Name  | Type    |
# +--------------+---------+
# | player_id    | int     |
# | device_id    | int     |
# | event_date   | date    |
# | games_played | int     |
# +--------------+---------+
# (player_id, event_date) is the primary key of this table.
# This table shows the activity of players of some game.
# Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on some day using some device.
