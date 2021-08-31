/*输入商铺名shopname，在PRODUCT表中查找商铺名为shopname的所有商品的商铺名、商品名、价格*/
create procedure FindItemInShop
@shopname nvarchar(30)
as
begin
	select SHOPNAME, PRONAME, PRICE
	from PRODUCT
	where SHOPNAME = @shopname
end
go

/*输入商品名关键词proname，在PRODUCT表中查找连续包含此关键词的所有商品的商铺名、商品名、价格*/
create procedure FindShopWithItem
@proname nvarchar(30)
as
begin
	select SHOPNAME, PRONAME, PRICE
	from PRODUCT
	where PRONAME like @proname
end
go

/*将（商铺名，商品名）加入某用户的购物车（若已存在则不操作）*/
create procedure AddTrolley
@username nvarchar(30), @shopname nvarchar(30), @proname nvarchar(30)
as
begin
	if not exists(select * from TROLLEY
			where USERNAME = @username and SHOPNAME = @shopname and PRONAME = @proname)
	 begin
		insert into TROLLEY values(@username, @shopname, @proname)
	 end
end
go

/*商铺往PRODUCT表中插入新商品，若已存在则更新价格信息*/
create procedure AddProduct
@shopname nvarchar(30), @proname nvarchar(30), @price float
as
begin
	if exists(select * from PRODUCT 
			where SHOPNAME = @shopname and PRONAME = @proname)
	 begin
		update PRODUCT
		set PRICE = @price
		where SHOPNAME = @shopname
		and PRONAME = @proname
	 end
	else
	 begin
		insert into PRODUCT values(@shopname, @proname, @price)
	end
end
go

/*改变PRODUCT表中指定（商铺名、商品名）的价格*/
create procedure AlterSinglePrice
@shopname nvarchar(30), @proname nvarchar(30), @price float
as
begin
	update PRODUCT
	set PRICE = @price
	where SHOPNAME = @shopname
	and PRONAME = @proname
end
go

/*按比例改变PRODUCT表中指定（商铺名，商品名）行的价格*/
create procedure AlterAllPrice
@shopname nvarchar(30), @percentage float
as
begin
	update PRODUCT
	set PRICE = PRICE * @percentage
	where SHOPNAME = @shopname
end
go

/*在PRODUCT表中删除指定（商铺名，商品名）的行【首先在TROLLEY表中删除对应的行】*/
create procedure DeleteProduct
@shopname varchar(30), @proname varchar(30)
as
begin
	delete from TROLLEY
	where SHOPNAME = @shopname
	and PRONAME = @proname
	delete from PRODUCT
	where SHOPNAME = @shopname
	and PRONAME = @proname
end
go

/*查看一个商铺的交易总收入，用group by rollup统计归类：先按照商品名归类，再按照买家所在地归类*/
create procedure CheckSale
@shopname varchar(30)
as
begin 
	select CONTAIN.PRONAME, CUSTOMER.LOC, sum(CONTAIN.PRICE) as TOTALPRICE
	from (CONTAIN join LIST on CONTAIN.NUM = LIST.NUM) join CUSTOMER on LIST.USERNAME = CUSTOMER.USERNAME
	where CONTAIN.SHOPNAME = @shopname
	group by rollup(CONTAIN.PRONAME, CUSTOMER.LOC)
end