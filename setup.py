from setuptools import find_packages, setup


def readfile(filename):
    with open(filename, "r+") as f:
        return f.read()


setup(
    name="run_dfm_report",
    version="2026.05.11",
    packages=find_packages(),
    description="Create a report of PubMed articles by DFM faculty",
    long_description=readfile("README.md"),
    author="Mihir Jagtap, Kevin J. Delaney",
    author_email="jagtapmihir4@gmail.com, kjdelaney@health.ucsd.edu",
    url="https://github.com/UCSD-Tai-Seale-Lab/DFM-Research-Paper-Digest",
    py_modules=["dfm_research_paper_digest", "query_faculty_batch"],
    license=readfile("LICENSE"),
    entry_points={
        "console_scripts": [
            "run_dfm_report = dfm_research_paper_digest.query_faculty_batch:main"
        ]
    },
)
