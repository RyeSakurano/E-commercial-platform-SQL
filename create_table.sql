create table CUSTOMER (
	USERNAME nvarchar(15),
	PWD nvarchar(30),
	PHONE varchar(15),
	LOC nvarchar(10),
	ADDR nvarchar(50),
	primary key (USERNAME)
)
go

create table SHOP (
	SHOPNAME nvarchar(15),
	PWD nvarchar(30),
	primary key (SHOPNAME)
)
go

create table PRODUCT (
	SHOPNAME nvarchar(15),
	PRONAME nvarchar(15),
	PRICE float,
	primary key (SHOPNAME, PRONAME),
	foreign key (SHOPNAME) references SHOP
)
go

create table LIST (
	NUM nvarchar(15),
	USERNAME nvarchar(15),
	primary key (NUM),
	foreign key(USERNAME) references CUSTOMER
)
go

create table CONTAIN (
	NUM nvarchar(15),
	SHOPNAME nvarchar(15),
	PRONAME nvarchar(15),
	PRICE float,
	foreign key (NUM) references LIST
)
go

create clustered
index idx_contain
on CONTAIN(NUM)
go

create table TROLLEY (
	USERNAME nvarchar(15),
	SHOPNAME nvarchar(15),
	PRONAME nvarchar(15),
	primary key (USERNAME, SHOPNAME, PRONAME),
	foreign key (USERNAME) references CUSTOMER,
	foreign key (SHOPNAME, PRONAME) references PRODUCT
)
go

/*
drop table CONTAIN
drop table TROLLEY
drop table CUSTOMER
drop table PRODUCT
drop table LIST
drop table SHOP*/



