drop table if exists events;
create table events (
	id integer primary key autoincrement,
	event_name text not null,
	mtg_format text not null
);
create table rounds (
	id integer primary key autoincrement,
	round_number integer,
	event_name text not null,
	FOREIGN KEY (event_name) REFERENCES events(event_name)
);
