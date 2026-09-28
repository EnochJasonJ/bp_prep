select r.region_name , sum(sales_amount) as total_sales
from regions r, sales s where r.region_id = s.region_id group by r.region_name ORDER BY total_sales DESC;

select * from sales;

select sr.sales_rep_name,sum(s.sales_amount) as total_sales, count(s.sales_rep_id) as transaction_count
from sales_reps sr
join sales s
on sr.sales_rep_id = s.sales_rep_id
GROUP BY sr.sales_rep_name
having count(s.sale_id) < 200
order by total_sales desc;

SELECT * from sales;

select 
    r.region_name, 
    sum(s.sales_amount) as total_sales, 
from regions r
join sales s
on r.region_id = s.region_id
group by r.region_name;

with region_sales AS (
    SELECT
        r.region_name,
        sum(s.sales_amount) as total_sales
    from regions r
    join sales s
        on r.region_id = s.region_id
    group by r.region_name
),

company_sales as (
    select
        sum(sales_amount) as company_total from sales
)

select 
    rs.region_name,
    rs.total_sales,
    (rs.total_sales / cs.company_total) * 100 as revenue_percentage
from region_sales rs
cross join company_sales cs;
-- select sum(sales_amount) as company_total from sales;