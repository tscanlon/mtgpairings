drop table if exists events;
create table events (
	id integer primary key autoincrement,
	event_name text not null,
	mtg_format text not null
);
drop table if exists rounds;
create table rounds (
	id integer primary key autoincrement,
	round_number integer,
	event_id integer not null,
	pairings text not null,
	FOREIGN KEY (event_id) REFERENCES events(id)
);
