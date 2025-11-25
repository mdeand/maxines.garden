PRAGMA user_version = 1;

create table entries (
  id integer primary key autoincrement,
  
  slug text unique not null,
  body text not null,  
  views integer default 0,
  content_md5_hash text not null,

  user_title text not null,
  user_description text not null,
  user_group text not null,
  user_date_created datetime default current_timestamp,
  user_date_modified datetime default current_timestamp,
  user_visibility integer default 1,
  user_draft integer default 0
  );

create index ix_entries_slug on entries (slug);

create table tags (
  id integer primary key autoincrement,
  name text unique not null
  );

create table entry_tags (
  entry_id integer not null references entries (id) on delete cascade,
  tag_id integer not null references tags (id) on delete cascade,
  primary key (entry_id, tag_id)
  );