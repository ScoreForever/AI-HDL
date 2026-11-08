@echo off
cd /d "%~dp0"
where xelatex >nul 2>nul
if errorlevel 1 (
 echo XeLaTeX not found. Add TeX Live bin to PATH and restart the terminal.
 exit /b 1
)
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=Lab1_Report_team01 report.tex
if errorlevel 1 exit /b 1
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=Lab1_Report_team01 report.tex
if errorlevel 1 exit /b 1
echo Created Lab1_Report_team01.pdf
