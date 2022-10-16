-- 1
    select player_id, device_id
    from Activity
    where (player_id, event_date) in (
        select player_id, min(event_date)
        from Activity
        group by player_id
    );
-- 2
    SELECT
        player_id,
        device_id
    FROM (
             SELECT
                 player_id,
                 device_id,
                 event_date,
                 MIN(event_date) OVER(PARTITION BY player_id ORDER BY event_date) as first_login
             -- We are partitioning the data by each player Id so that we get
             -- a separate first login date for each user and
             -- also ordering the event_date in ascending order to get the earliest date
             -- when the user first logged In.
             FROM Activity
         ) t1
    WHERE event_date = first_login;
-- via: https://lifewithdata.com/2021/08/03/sql-interview-questions-leetcode-512-game-play-analysis-ii/


# 请编写一个SQL查询，描述每一个玩家首次登陆的设备名称
#
# 查询结果格式在以下示例中：
# Activity table:
# |player_id | device_id | event_date | games_played |
