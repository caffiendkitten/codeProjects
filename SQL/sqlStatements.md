# Dont forget about UNION

The UNION statement is used to put together information from two requests: `SELECT * FROM articles WHERE id=3 UNION SELECT ...` Since it is used to retrieve information from other tables, it can be used as a SQL injection payload. When the beginning of the query can't be modify directly by the attacker, maybe since it's generated by the PHP code. However using UNION, the attacker can manipulate the end of the query and retrieve information from other tables:

`SELECT id,name,price FROM articles WHERE id=3  
UNION SELECT id,login,password  FROM users`

Note: The most important rule, is that both statements should return the same number of columns otherwise the database will trigger an error.

Exploiting SQL injection using UNION follows the steps below:
1. Find the number of columns to perform the UNION
2. Find what columns are echoed in the page
3. Retrieve information from the database meta-tables
4. Retrieve information from other tables/databases

In order to perform a request by SQL injection, you need to find the number of columns that are returned by the first part of the query. Unless you have the source code of the application, you will have to guess this number.

There are two methods to get this information:

using UNION SELECT and increase the number of columns;
using ORDER BY statement.