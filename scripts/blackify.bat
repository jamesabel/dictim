pushd .
cd ..
call venv\Scripts\activate.bat
python -m black -l 192 dictim test_dictim examples setup.py
call deactivate
popd
