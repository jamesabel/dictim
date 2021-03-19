pushd .
cd ..
call venv\Scripts\activate.bat 
mypy -m dictim
call deactivate
popd
