insert into people values
('0', 'Chandler Bing', 170, 170, 'grey', 'brown',
'123 4 St, Edmonton', 'm', date '69-11-13' );

insert into people values
('1', 'Monica Bing', 162, 150, 'blue', 'black',
'123 4 St, Edmonton', 'f', date '70-06-03');

insert into people values
('2', 'Erica Bing', 163, 140, 'blue', 'brown',
'567 4 Ave, Calgary', 'f', date '95-03-03');

insert into people values
('3', 'Rachel Green', 163, 140, 'grey', 'bronze',
'3 abc Ave, Calgary', 'f', date '70-08-10');

insert into people values
('4', 'Mujda Abbasi', 162, 136, 'brown', 'black',
'356 123 Ave, Edmonton', 'f', date '93-08-10');

insert into people values
('088', 'Officer', 162, 136, 'brown', 'black',
'356 123 Ave, Edmonton', 'm', date '90-08-10');


insert into drive_licence values
(0000, 0,'5',null,date '15-03-01',date '20-03-01');

insert into drive_licence values
(0001, 1,'5',null,date '14-06-01',date '19-03-01');

insert into drive_licence values
(0002, 2,'5',null,date '15-11-01',date '20-11-01');

insert into drive_licence values
(0003, 3,'5',null,date '13-03-01',date '18-03-01');

insert into drive_licence values
(0004, 4, 'nondriving', null, date '14-03-01', date '19-03-01');




insert into vehicle_type values
('0', 'SUV');

insert into vehicle_type values
('1', 'Sedan');




insert into vehicle values
('0', 'Dodge', 'Grand Caravan', '2000', 'blue', '0');

insert into vehicle values
('1', 'Mitsubishi', 'Outlander', '2004', 'black', '0');

insert into vehicle values
('2', 'Toyota', 'Land Cruiser', '2009', 'black', '0');

insert into vehicle values
('3', 'Toyota', 'Corola', '2009', 'red', '1');




insert into owner values
('0', '0', 'y');

insert into owner values
('0', '1', 'y');

insert into owner values
('0', '2', 'y');

insert into owner values
('1', '0', 'n');

insert into owner values
('1', '1', 'n');

insert into owner values
('1', '2', 'n');

insert into owner values
('2', '2', 'n');

insert into owner values
('3', '3', 'y');




insert into auto_sale values
('00','3', '0', '0', date '10-01-04', 10000);

insert into auto_sale values
('01','3', '0', '1', date '10-06-05', 5000);

insert into auto_sale values
('02','0', '3', '3', date '11-06-05', 3000);




insert into ticket_type values
('speeding', 500);


insert into ticket values
('0', '3', '3', '088', 'speeding', date '15-07-02', '134 24 ave, Calgary', '10 over speed limit');

insert into ticket values
('1', '3', '3', '088', 'speeding', date '15-06-05', '567 23 ave, Calgary', '10 over speed limit');

insert into ticket values
('2', '3', '3', '088', 'speeding', date '15-04-23', '123 xyz ave, Calgary', '10 over speed limit');



