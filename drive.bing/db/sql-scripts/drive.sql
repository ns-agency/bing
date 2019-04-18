DROP DATABASE IF EXISTS drive;
CREATE DATABASE drive;

use drive;

DROP TABLE IF EXISTS users;

CREATE TABLE users (
  username TEXT,
  password TEXT,
  role TEXT
);

DROP TABLE IF EXISTS files;

CREATE TABLE files (
  id SERIAL PRIMARY KEY,
  name TEXT,
  content TEXT,
  author TEXT
);

INSERT INTO files(name,content,author) VALUES ('flag', 'BREAK2{cheeky_bugger_u_aint_fixed_the_bug_innit}, Note to self, delete /admin','admin'),
  ('staff_api_a456h7dvra','BREAK2{call_the_govnr_we_got_ourselfs_a_hacker_innit} also /staff/secret/1gbdfte/swagger','staff_account');

INSERT INTO users VALUES ('testStaff', 'testStaff', 'Staff');

DROP USER IF EXISTS 'driveuser'@'%';

CREATE USER 'driveuser'@'%' IDENTIFIED WITH mysql_native_password BY '4e34134344b-5834242a-9229-ddf2d6432426b0c45';
GRANT SELECT, INSERT, UPDATE ON *.* TO 'driveuser'@'%';
GRANT FILE on *.* TO 'driveuser'@'%';
FLUSH PRIVILEGES;
