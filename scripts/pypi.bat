pushd .
cd ..
del /Q dictim.egg-info\*.*
del /Q build\*.*
del /Q dist\*.*
copy /Y LICENSE LICENSE.txt
call venv\Scripts\activate.bat
python.exe setup.py bdist_wheel
twine upload dist/*
rmdir /Q /S build
rmdir /Q /S dist
rmdir /Q /S dictim.egg-info
call deactivate
popd
