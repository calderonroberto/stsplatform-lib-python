import setuptools
import textwrap
import subprocess
import shutil
import os.path

version = "0.1.0"

if __name__ == "__main__":
    setuptools.setup(
        name="stsplatform",
        version=version,
        description="Use the SenseTecnic Systems Platform API",
        author="Roberto Calderon",
        author_email="rcalderon@sensetecnic.com",
        url="https://github.com/SenseTecnic/stsplatform-lib-python",
        long_description=textwrap.dedent("""\
            Quick Tutorial
            ==============

            First import the library:
                import stsplatform.client as sts
            Create an STS Platform client:
                w = sts.Client()
            Print a sensor hosted in the platform
                s = sts.Sensors(w,'mike.yvr-arrive')
                print s.get().data
            Print some data (last data point)
                d = sts.Data(s)
                print d.get({'beforeE':1}).data
            More Help
            =========
            See http://developers.sensetecnic.com"""),
        packages=[
            "stsplatform",
            "stsplatform.tests",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Topic :: Software Development",
        ],
        install_requires=[
          'requests'
        ],
        test_suite="stsplatform.tests",
    )
