--1. Отримати всі завдання певного користувача

select * from tasks t where user_id = 1;

--2. Вибрати завдання за певним статусом 

select * 
from tasks t 
where status_id = (select id from status where name = 'new'); 

--3. Оновити статус конкретного завдання

update tasks 
set status_id = (select id from status where name = 'in progress')
where id = 20;

--4. Отримати список користувачів, які не мають жодного завдання

select * from users where id not in (select distinct user_id from tasks t);

--5. •	Додати нове завдання для конкретного користувача

insert into tasks (title, description, status_id, user_id) 
values (
	'Dream.', 
	'Go to bed early', 
	(select id from status where name = 'new'), 1)
	
--6. Отримати всі завдання, які ще не завершено
	
select * 
from tasks t 
where status_id != (select id from status s where name = 'completed');
	
--7. Видалити конкретне завдання

delete from tasks where id = 21;

--8. Знайти користувачів з певною електронною поштою

select * from users u 
where email like '%tdelacruz@example.com';
	
--9. Оновити ім'я користувача

update users set fullname = 'Maryna Korbet' where id = 1;

--10. Отримати кількість завдань для кожного статусу

select s.name, count(t.id) as tasks_count
from status s 
left join tasks t on s.id = t.status_id  
group by s.name;

--11 Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти

select *
from tasks t 
inner join users u  on t.user_id = u.id
where u.email like '%example.com';

--12. Отримати список завдань, що не мають опису

select * from tasks t where description = '' or description is null;

--13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'

select t.*, u.*
from users u 
inner join tasks t on u.id  = t.user_id 
inner join  status s on s.id = t.status_id 
where s.name = 'in progress';

--14. Отримати користувачів та кількість їхніх завдань

select u.fullname , count(t.id) as tasks_count
from users u 
left join tasks t on u.id = t.user_id 
group by u.id;

