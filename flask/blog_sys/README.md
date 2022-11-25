## Learn

flask: https://dormousehole.readthedocs.io/en/latest/

- demo: https://dormousehole.readthedocs.io/en/latest/tutorial

Jinja2: http://docs.jinkan.org/docs/jinja2/

## TestUrl

- http://127.0.0.1:5000/index
- http://127.0.0.1:5000/auth/login

## Setup

应用部署至服务器

① github / gitee

② 发行文件 wheel `(.whl)`

- 库安装

```powershell
pip install wheel
```

- 发行文件构建

```powershell
python setup.py bdist_wheel
```

在`dist`目录下输出文件: `{project name}-{version}...`

setup.py

```python
from setuptools import find_packages, setup

setup(
    name='app_name', # 项目名
    version='1.0.0', # 版本号
    packages=find_packages(),
    # 导入 python package
    # ( __init__.py 所在的同级目录下所有的 py 文件 )
    include_package_data=True,
    # 导入 MANIFEST.in 所指定的文件
    zip_safe=False,
    install_requires=[ # 依赖库
        'flask',
    ],
)
```

MANIFEST.in

```MANIFEST
include main/schema.sql
graft main/static
graft main/templates
global-exclude *.pyc
```

include: 包含指定文件

graft: 包含目录及其子目录

global-exclude: 全局排除

- 新环境中部署

```powershell
pip install main-1.0.0-py3-none-any.whl
```
