drop table if exists restaurant;
create table restaurant (
  r_id integer primary key autoincrement,
  rname text not null,
  data text not null
);

drop table if exists menu;
create table menu (
  m_id integer primary key autoincrement,
  r_id integer,
  data text not null,
  type integer,
  parent_m_id integer,
  child_m_id text
);

