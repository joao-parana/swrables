@echo off
set repetions=%1
echo Executing %repetions% iterations
for /L %%i in (1,1,%repetions%) do (
echo Iteration #%%i
python turbodiag.py
)