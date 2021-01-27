# escape=`

ARG FROM_IMAGE=mcr.microsoft.com/dotnet/framework/sdk:4.8
FROM ${FROM_IMAGE} as certsgen
RUN certutil -generateSSTFromWU roots.sst

FROM ${FROM_IMAGE} as BASE_BUILDER

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop';"]

ARG CHOCOLATEY_SOURCE=https://chocolatey.org/api/v2
ARG ChocolateyEnvironmentDebug=false
ADD ci/docker/python/share/install_choco.ps1 choco/install_choco.ps1
RUN Set-ExecutionPolicy Bypass -Scope Process -Force; `
    ./choco/install_choco.ps1 -packageRepo $env:CHOCOLATEY_SOURCE ; `
    if( -not ([string]::IsNullOrEmpty($Env:CHOCOLATEY_SOURCE ))) `
    { `
        Write-Host "Adding $env:CHOCOLATEY_SOURCE to chocolatey sources" ; `
        choco source add -n=CHOCOLATEY_SOURCE --priority=1 -s=\"$env:CHOCOLATEY_SOURCE\"; `
        choco source remove -n=chocolatey ;`
    }; `
    Write-Host "Disabling Showing Download Progress" ; `
    choco feature disable -n=showDownloadProgress ; `
    Remove-Item C:\ProgramData\chocolatey\bin\cpack.exe ; `
    Remove-Item -Force -Recurse ${Env:TEMP}\*


ADD ci/docker/shared/chocolatey/packages.config choco/packages.config
RUN C:\ProgramData\chocolatey\bin\choco.exe sources ; `
    C:\ProgramData\chocolatey\bin\choco.exe install -y --stoponfirstfailure --no-progress --verbose choco/packages.config ;`
    Remove-Item C:\Users\ContainerAdministrator\AppData\Local\Temp\chocolatey -Recurse ; `
    refreshenv ; `
    Remove-Item -Force -Recurse ${Env:TEMP}\* ; `
    if (!(Test-Path 'C:\Program Files\Git\cmd\git.exe')) `
    { `
        throw 'git.exe not found' ; `
    }; `
    Write-Host "Finished install packages with Chocolatey"


ADD ci/docker/python/windows/build/msvc/pythonVersions.xml choco/python.config
RUN Write-Host "Installing Python $PYTHON_VERSION with Chocolatey" ; `
    $process = start-process -NoNewWindow -PassThru -FilePath C:\ProgramData\chocolatey\bin\choco.exe -ArgumentList 'install -y --stoponfirstfailure --no-progress --verbose choco/python.config', "-my" -Wait ;`
    if ( $process.ExitCode -eq 0) `
        { `
            Write-Host "Installing Python $PYTHON_VERSION with Chocolatey - Done" ; `
        } else { `
            throw "Installing packages with Chocolatey - Failed with exit code ($process.ExitCode)" ;  `
        };`
    Remove-Item C:\Users\ContainerAdministrator\AppData\Local\Temp\chocolatey -Recurse ; `
    py --list


# ==============================================================================
FROM BASE_BUILDER as WHEEL_BUilDER_PY36
SHELL ["cmd", "/S", "/C" ]
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
COPY requirements.txt  requirements-dev.txt ci/docker/python/share/requirements-ci.txt c:/requirements/
ENV PY_PYTHON=3.6
RUN py -m pip install --upgrade pip wheel && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-ci.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-dev.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements.txt

# ==============================================================================
FROM BASE_BUILDER as WHEEL_BUilDER_PY37
SHELL ["cmd", "/S", "/C" ]
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
COPY requirements.txt  requirements-dev.txt ci/docker/python/share/requirements-ci.txt c:/requirements/
ENV PY_PYTHON=3.7
RUN py -m pip install --upgrade pip wheel && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-ci.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-dev.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements.txt

# ==============================================================================
FROM BASE_BUILDER as WHEEL_BUilDER_PY38
SHELL ["cmd", "/S", "/C" ]
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
COPY requirements.txt  requirements-dev.txt ci/docker/python/share/requirements-ci.txt c:/requirements/
ENV PY_PYTHON=3.8
RUN py -m pip install --upgrade pip wheel && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-ci.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-dev.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements.txt


# ==============================================================================
FROM BASE_BUILDER as WHEEL_BUilDER_PY39
SHELL ["cmd", "/S", "/C" ]
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
COPY requirements.txt  requirements-dev.txt ci/docker/python/share/requirements-ci.txt c:/requirements/
ENV PY_PYTHON=3.9
RUN py -m pip install --upgrade pip wheel && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-ci.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements-dev.txt && `
    py -m pip wheel -w c:\wheels\ --no-cache-dir -r c:/requirements/requirements.txt

# ==============================================================================
FROM BASE_BUILDER
COPY --from=certsgen c:/roots.sst roots.sst
RUN certutil -addstore -f root roots.sst ; `
    del roots.sst

COPY --from=WHEEL_BUilDER_PY36 c:/wheels/ c:/wheels/
COPY --from=WHEEL_BUilDER_PY37 c:/wheels/ c:/wheels/
COPY --from=WHEEL_BUilDER_PY38 c:/wheels/ c:/wheels/
COPY --from=WHEEL_BUilDER_PY39 c:/wheels/ c:/wheels/

ENV PIP_FIND_LINKS=c:\wheels

RUN python -m pip install pip --upgrade ; pip install tox
WORKDIR C:/src
CMD tox --workdir ${Env:TEMP}\tox\ -vv  --recreate