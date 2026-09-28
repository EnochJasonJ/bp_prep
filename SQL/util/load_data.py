import pandas as pd
import psycopg2

csv_path = "sales_data.csv"

conn = psycopg2.connect(
    dbname="sales_analytics",
    user="enochjason",
)

df = pd.read_csv(csv_path)
df = df.drop(columns=["Region_and_Sales_Rep"])
print(f"Loaded {len(df)} rows")

print(df.shape)
print(df.columns.tolist())

print("Sales Reps:", df["Sales_Rep"].unique())
print("Regions:",df["Region"].unique())
print("Categories:",df["Product_Category"].unique())
print("Customer Types:",df["Customer_Type"].unique())
print("Payment Methods:",df["Payment_Method"].unique())
print("Sales Channels:", df["Sales_Channel"].unique())

def insert_dimension(cur,table,column,values):
    for value in values:
        cur.execute(
            f"""
            insert into {table} ({column})
            values (%s)
            on conflict ({column}) do nothing
            """,
            (value,)
        )

with conn.cursor() as cur:
    insert_dimension(
        cur,
        "regions",
        "region_name",
        df["Region"].unique()
    )
    insert_dimension(
        cur,
        "categories",
        "category_name",
        df["Product_Category"].unique()
    )
    insert_dimension(
        cur,
        "customer_types",
        "customer_type_name",
        df["Customer_Type"].unique()
    )
    insert_dimension(
        cur,
        "payment_methods",
        "payment_method_name",
        df["Payment_Method"].unique()
    )
    insert_dimension(
        cur,
        "sales_channels",
        "sales_channel_name",
        df["Sales_Channel"].unique()
    )
    conn.commit()

with conn.cursor() as cur:
    cur.execute("select * from sales_reps")
    print(cur.fetchall())
    cur.execute("SELECT * FROM regions")
    print(cur.fetchall())
    cur.execute("SELECT * FROM categories")
    print(cur.fetchall())
    cur.execute("SELECT * FROM customer_types")
    print(cur.fetchall())
    cur.execute("SELECT * FROM payment_methods")
    print(cur.fetchall())
    cur.execute("SELECT * FROM sales_channels")
    print(cur.fetchall())

with conn.cursor() as cur:
    for _, row in df.iterrows():
        cur.execute(
            """
            insert into sales(
            sale_date, product_id, sales_rep_id, region_id, category_id, customer_type_id,
            payment_method_id, sales_channel_id, sales_amount,
            quantity_sold, unit_cost, unit_price, discount
            )
            values(
            %s,
            %s,
            (select sales_rep_id from sales_reps where sales_rep_name = %s),
            (select region_id from regions where region_name = %s),
            (select category_id from categories where category_name = %s),
            (select customer_type_id from customer_types where customer_type_name = %s),
            (select payment_method_id from payment_methods where payment_method_name = %s),
            (select sales_channel_id from sales_channels where sales_channel_name = %s),
            %s, %s, %s, %s, %s
            )
            """,
            (
                row["Sale_Date"],
                row["Product_ID"],
                row["Sales_Rep"],
                row["Region"],
                row["Product_Category"],
                row["Customer_Type"],
                row["Payment_Method"],
                row["Sales_Channel"],
                row["Sales_Amount"],
                row["Quantity_Sold"],
                row["Unit_Cost"],
                row["Unit_Price"],
                row["Discount"]
            )
        )
    conn.commit()
print("Sales data inserted successfully!")