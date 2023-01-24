from setuptools import setup, find_packages

VERSION = '0.0.6'
DESCRIPTION = 'User management authentiation'

try:
    # read the contents of README file
    from pathlib import Path
    this_directory = Path(__file__).parent
    LONG_DESCRIPTION = (this_directory / "README.md").read_text()
except:
    LONG_DESCRIPTION = 'User management authentication and authorization for FastAPI using AWS Cognito service'

# Setting up
setup(
        name="fastauth", 
        version=VERSION,
        author="Ofry Makdasy",
        author_email="ofry.makdsy@tech-19.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[
            'fastapi',
            'python-dotenv==0.21.0',
            'python-jose==3.3.0',
            'requests==2.28.2',
            'SQLAlchemy==1.4.46',
            'psycopg2',
            'boto3',
            ],
        
        keywords=['python', 'first package' , 'fastapi' , 'cognito' , 'jwt'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)