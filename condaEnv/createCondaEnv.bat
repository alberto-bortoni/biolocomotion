:: CREATE CONDA ENVIRONMENT FOR VIDEO STACKS
@echo off
cls

::-------------------------------------------------------------------
:: READ FILE
SET cfile=%1
set _ext=%~x1

ECHO Configuration file input: 
ECHO %cfile%
ECHO.

::-------------------------------------------------------------------
:: test to see if file is there
IF EXIST %cfile% (
  IF "%_ext%" EQU ".yml" (
    GOTO installConda
  ) ELSE (
      ECHO config file must be a .yml file... exiting
      EXIT /B
  )
) ELSE (
    ECHO config file does not exist or was not provided... exiting
    EXIT /B
)


::-------------------------------------------------------------------
:: Install conda environmant or update if exists
:installConda

ECHO installing conda dependencies
ECHO.
::conda env list
CALL conda env update -f condaConfig.yml --prune

ECHO Installed, now activating environment
CALL conda activate batConda

ECHO exiting =)
EXIT /B

:: EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF EOF