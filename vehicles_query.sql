-- KeepCoding active vehicles query
select m.model_name "Modelo", mk.make_name "Marca", g.group_name "Grupo", v.purchase_date "Fecha de compra",
	   v.number_plate "Matrícula", v.color "Color", v.kilometers "Kilómetros", 
	   ic.insurance_company_name "Aseguradora", v.insurance_policy_number "Número de póliza"
from keepcoding.vehicles v
join keepcoding.models m on v.model_id = m.model_id
join keepcoding.makes mk on m.make_id = mk.make_id
join keepcoding.groups g on mk.group_id = g.group_id
join keepcoding.insurance_companies ic on v.insurance_company_id = ic.insurance_company_id
where v.deregistration_date = '4000-01-01';

