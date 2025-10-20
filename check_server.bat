@echo off
echo ===============================================
echo    VERIFICACAO RAPIDA - SERVIDOR PULSE
echo ===============================================
echo.

echo [1/3] Verificando se o servidor esta rodando...
curl -s -o nul -w "Status: %%{http_code}" http://127.0.0.1:8000/ 2>nul
if %errorlevel% equ 0 (
    echo  - ✅ Servidor respondendo
) else (
    echo  - ❌ Servidor nao esta respondendo
)

echo.
echo [2/3] Testando pagina principal...
curl -s -o nul -w "Status: %%{http_code}" http://127.0.0.1:8000/consultorio/ 2>nul
if %errorlevel% equ 0 (
    echo  - ✅ Dashboard medico funcionando
) else (
    echo  - ❌ Dashboard com problema
)

echo.
echo [3/3] Testando admin...
curl -s -o nul -w "Status: %%{http_code}" http://127.0.0.1:8000/admin/ 2>nul
if %errorlevel% equ 0 (
    echo  - ✅ Admin Django funcionando
) else (
    echo  - ❌ Admin com problema
)

echo.
echo ===============================================
echo    SISTEMA PULSE - STATUS VERIFICADO
echo ===============================================
echo.
echo Para iniciar o servidor:    python manage.py runserver
echo Para acessar o sistema:     http://127.0.0.1:8000/consultorio/
echo Para acessar o admin:       http://127.0.0.1:8000/admin/
echo.
pause