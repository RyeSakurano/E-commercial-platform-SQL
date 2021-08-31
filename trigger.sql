/*触发器：在发生购买时（更新CONTAIN表）同时，要删除TROLLEY表中用户购物车信息*/
create trigger MakePurchaseFromTrolley
on CONTAIN
after insert
as
declare @num nvarchar(15)
declare @shopname nvarchar(15)
declare @proname nvarchar(15)
select @num=NUM, @shopname=SHOPNAME, @proname=PRONAME
from inserted
delete from TROLLEY 
where TROLLEY.USERNAME = (select USERNAME from LIST where NUM = @num)
and SHOPNAME=@shopname
and PRONAME=@proname