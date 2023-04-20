import setuptools

setuptools.setup(name="agent9",
                 packages=setuptools.find_packages(exclude=["test"]),
                 version="1.0.0",
                 author="Tuan Nguyen Minh",
                 author_email="tuana9a@gmail.com",
                 entry_points={
                     "console_scripts": [
                         "agent9=agent9.cmd.server:main",
                         "agent9-tools=agent9.cmd.tools:main"
                     ]
                 },
                 install_requires=[
                     "docker==5.0.3", "crossplane==0.5.8", "requests==2.28.0",
                     "fastapi==0.85.0", "uvicorn==0.18.3"
                 ])
