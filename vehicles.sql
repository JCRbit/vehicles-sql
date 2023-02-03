create schema keepcoding;

-- Create tables
create table keepcoding.vehicles(
	vehicle_id varchar(10) not null,
	purchase_date date not null,
	deregistration_date date not null default '4000-01-01',
	model_id varchar(20) not null, --FK
	color varchar(50) not null,
	number_plate varchar(30) not null unique,
	kilometers numeric(8,2) not null check(kilometers >= 0),
	insurance_policy_number varchar(10) not null,
	insurance_company_id varchar(10) not null, --FK
	constraint vehicles_pk primary key(vehicle_id)
);

create table keepcoding.models(
	model_id varchar(20) not null,
	model_name varchar(50) not null,
	make_id varchar(10) not null, --FK
	constraint models_pk primary key(model_id)
);

create table keepcoding.makes(	
	make_id varchar(10) not null,
	make_name varchar(100) not null,
	group_id varchar(10) not null, --FK
	constraint makes_pk primary key(make_id)
);

create table keepcoding.groups(
	group_id varchar(10) not null,
	group_name varchar(100) not null,
	constraint groups_pk primary key(group_id)
);

create table keepcoding.insurance_companies(
	insurance_company_id varchar(10) not null,
	insurance_company_name varchar(100) not null,
	constraint insurance_companies_pk primary key(insurance_company_id)
);

create table keepcoding.checkups(
	checkup_id varchar(20) not null,
	vehicle_id varchar(10) not null, --FK
	checkup_date date not null,
	kilometers numeric(8,2) not null check(kilometers >= 0),
	checkup_cost numeric(7,2) not null,
	currency_id varchar(10) not null, --FK
	constraint checkups_pk primary key(checkup_id)
);
	
create table keepcoding.currencies(
	currency_id varchar(10) not null,
	currency_name varchar(50) not null,
	currency_code varchar(10) not null,
	constraint curencies_pk primary key(currency_id)
);

-- Add foreign keys
alter table keepcoding.vehicles
	add constraint vehicles_models_fk foreign key(model_id) references keepcoding.models(model_id),
	add constraint vehicles_insurance_companiess_fk foreign key(insurance_company_id) references keepcoding.insurance_companies(insurance_company_id);
	
alter table keepcoding.models
	add constraint models_makes_fk foreign key(make_id) references keepcoding.makes(make_id);
	
alter table keepcoding.makes
	add constraint makes_groups_fk foreign key(group_id) references keepcoding.groups(group_id);

alter table keepcoding.checkups
	add constraint checkups_vehicles_fk foreign key(vehicle_id) references keepcoding.vehicles(vehicle_id),
	add constraint checkups_currencies_fk foreign key(currency_id) references keepcoding.currencies(currency_id);
