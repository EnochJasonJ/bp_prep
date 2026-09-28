create table sales_reps(
    sales_rep_id serial PRIMARY KEY,
    sales_rep_name Varchar(50) UNIQUE NOT NULL
);

create table regions(
    region_id serial PRIMARY KEY,
    region_name varchar(50) unique NOT NULL
);

create table categories(
    category_id serial PRIMARY KEY,
    category_name varchar(50) UNIQUE NOT NULL
);

create table customer_types(
    customer_type_id serial PRIMARY KEY,
    customer_type_name varchar(50) UNIQUE NOT NULL
);

create table payment_methods (
    payment_method_id serial primary KEY,
    payment_method_name varchar(50) unique NOT NULL
);

create table sales_channels (
    sales_channel_id serial primary KEY,
    sales_channel_name varchar(50) UNIQUE NOT NULL
);

create table sales(
    sale_id serial PRIMARY KEY,
    sale_date date not null,
    product_id int not null,

    sales_rep_id int not null references sales_reps(sales_rep_id),
    region_id int not null references regions(region_id),
    category_id int not null references categories(category_id),
    customer_type_id int not null references customer_types(customer_type_id),
    payment_method_id int not null references payment_methods(payment_method_id),
    sales_channel_id int not null references sales_channels(sales_channel_id),

    sales_amount numeric(12,2) not null,
    quantity_sold int not null,
    unit_cost numeric(12,2) not null,
    unit_price numeric(12,2) not null,
    discount numeric(5,4) not null
);