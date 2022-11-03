create DATABASE BigDataSQL;

show databases;
create database test;
drop DATABASE test;

use BigDataSQL;
show tables;

create table test(age int, name VARCHAR(20));
select * from test;
insert into test values(24,'Mary');

show create table test;

drop table test;
show tables;

create table if not exists employee(
    id int,
    name VARCHAR(50),
    salary DOUBLE,
    hiring_date date
);


insert into employee values(1,'Vijay',50000,'2021-10-04');
select * from employee;

insert into employee(id,name) values(2,'Kumar');

insert into employee values (3,'Vijay',50000,'2021-10-04'),(4,'Vijay',50000,'2021-10-04'),(5,'Vijay',50000,'2021-10-04');

create table if not exists emp(
    id int not null,
    name VARCHAR(40) not null,
    salary double,
    hiring_date date DEFAULT '2022-01-01',
    unique(id),
    check(salary > 500)
);


insert into emp(id, name, salary) values(1,'Vijay',5000);
select * from emp;

create table if not exists emp1(
    id int not null,
    name VARCHAR(40) not null,
    salary double,
    hiring_date date DEFAULT '2022-01-01',
    constraint unique_id unique(id),
    constraint salary_check check(salary > 500)
);


