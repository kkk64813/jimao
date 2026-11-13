@echo off
chcp 65001 >nul
title 幾貓 加密打包
python "%~dp0打包.py"
if errorlevel 1 pause
