SELECT
        id, company, salary,
        COUNT(*) OVER (PARTITION BY company) cnt,
        ROW_NUMBER() OVER (PARTITION BY company ORDER BY salary) rnum
FROM employee e
WHERE (cnt/2) <= rnum AND rnum<= (cnt/2) + 1
ORDER BY company, salary;

select id, company, salary
from (
         select
             id,
             company,
             row_number() over(partition by company order by salary) rk,
             count(*) over(partition by company) as total
         from employee
     ) tmp
where tmp.rk in (floor((total + 1) / 2), floor((total + 2) / 2));

# Write a SQL query to find the median salary of each company.
# Bonus points if you can solve it without using any built-in SQL functions.
# 写一个SQL查询，找出每个公司的工资中位数。以任意顺序 返回结果表。
# Table: Employee
# +-----+------------+--------+
# |Id   | Company    | Salary |
# +-----+------------+--------+
# |1    | A          | 2341   |
# # |2    | A          | 341    |
# # |3    | A          | 15     |
# # |4    | A          | 15314  |
# # |5    | A          | 451    |
# # |6    | A          | 513    |
# |7    | B          | 15     |
# |8    | B          | 13     |
# |9    | B          | 1154   |
# |10   | B          | 1345   |
# |11   | B          | 1221   |
# |12   | B          | 234    |
# |13   | C          | 2345   |
# |14   | C          | 2645   |
# |15   | C          | 2645   |
# |16   | C          | 2652   |
# |17   | C          | 65     |
# +-----+------------+--------+

# +-----+------------+--------+
# |Id   | Company    | Salary |
# +-----+------------+--------+
# |5    | A          | 451    |
# |6    | A          | 513    |
# |12   | B          | 234    |
# |9    | B          | 1154   |
# |14   | C          | 2645   |
# +-----+------------+--------+
# via: https://medium.com/learn-from-data/leetcode-569-median-employee-salary-d9653d82048c
# https://blog.csdn.net/qq_42397330/article/details/123652086

