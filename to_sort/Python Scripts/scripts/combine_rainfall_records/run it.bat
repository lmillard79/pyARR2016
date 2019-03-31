del *.txt


copy aws_params.in parameters.in
rem copy daily_params.in parameters.in
rem copy pluvio_params.in parameters.in

python combine_rainfall.py

pause