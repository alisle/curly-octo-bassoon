#!/bin/zsh

echo "first name, last name, email, phone number"
for i in {1..300}
do
  first_name=$(shuf -n 1 male_first_names.txt)
  second_name=$(shuf -n 1 surnames.txt)
  company=$(shuf -n 1 domain_names.txt)
  email=$first_name.$second_name\@$company
  area_code=$(shuf -n 1 usa_phone_area_codes.txt )
  phone="+1 ($area_code) $(shuf -i 100-999 -n 1)-$(shuf -i 1000-9999 -n 1)"
  echo $first_name, $second_name,$email,$phone
done
