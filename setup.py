from setuptools import setup
import re


version = ""
with open("askitsu/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

# from discord.py
if version.endswith(("a", "b")) or version.startswith("0"):
    try:
        import subprocess

        p = subprocess.Popen(
            ["git", "rev-parse", "--short", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = p.communicate()
        if out:
            version += "+g" + out.decode("utf-8").strip()
    except Exception:
        pass

readme = ""
with open("README.md", encoding="utf-8") as f:
    readme = f.read()

packages = ["askitsu"]

setup(
    name="askitsu",
    author="ShomyKohai",
    version=version,
    license="MIT",
    description="An async python wrapper Kitsu.io API",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=packages,
    keywords=["kitsu", "kitsu api", "kitsu.io", "async"],
    install_requires=["aiohttp", "colorama"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
    project_urls={
        "Documentation": "https://askitsu.rtfd.org/",
        "Source": "https://github.com/ShomyKohai/askitsu",
    },
)
