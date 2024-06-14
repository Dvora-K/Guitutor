@echo off
if "%~2"=="" (
    echo You must provide input and output
    exit /b 1
)
echo start lala.ai
echo %1
echo %2
set INPUT=%1
set OUTPUT=%2

echo %cd%

icacls "C:\Users\User\Desktop\Guitutor\lalalai-master\tools\api\lalalai_splitter.py" /grant:r %username%:F

echo %INPUT%
echo %OUTPUT%
python "C:\Users\User\Desktop\Guitutor\lalalai-master\tools\api\lalalai_splitter.py" --input "%INPUT%" --license 443fd9d4db204667 --output "%OUTPUT%" --stem "acoustic_guitar"
