#!/bin/bash

xls_path="${XL_IDP_PATH_AUTO_TRACKING}/"

done_path="${xls_path}"/done
if [ ! -d "$done_path" ]; then
  mkdir "${done_path}"
fi

find "${xls_path}" -maxdepth 1 -type f \( -name "*.xls*" -or -name "*.XLS*" -or -name "*.xml" \) ! -newermt '3 seconds ago' -print0 | while read -d $'\0' file
do

  if [[ "${file}" == *"error_"* ]];
  then
    continue
  fi

	mime_type=$(file -b --mime-type "$file")
  echo "'${file} - ${mime_type}'"

	# Will convert csv to json
	python3 ${XL_IDP_PATH_AUTO_TRACKING_SCRIPTS}/scripts/main.py "${file}"

  if [ $? -eq 0 ]
	then
	  mv "${file}" "${done_path}"
	else
	  mv "${file}" "${xls_path}/error_$(basename "${file}")"
	fi

done