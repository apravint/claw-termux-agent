from setuptools import setup, find_packages

setup(
    name="claw-termux-agent",
    version="1.0.0",
    description="Autonomous Web Automation, Headless Scraping & AI Workflow Daemon Tuned for Termux & Linux",
    author="Pravin Tamilan (@apravint)",
    author_email="apravint@users.noreply.github.com",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
    ],
    entry_points={
        "console_scripts": [
            "clawagent = clawagent.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)
