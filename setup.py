from setuptools import setup, find_packages

from healthcheck_python.release import __version__, __author__


def read_file(file_name):
	"""Read file and return its contents."""
	with open(file_name, "r") as f:
		return f.read()


def read_requirements(file_name):
	"""Read requirements file as a list."""
	reqs = read_file(file_name).splitlines()
	if not reqs:
		raise RuntimeError(
			f"Unable to read requirements from the {file_name} file"
			"That indicates this copy of the source code is incomplete."
		)
	return reqs


setup(
	name="healthcheck-python",
	version=__version__,
	url="https://github.com/cagdasbas/healthcheck-python",
	python_requires='>=3.6',
	description="Health Check API for multiprocessing python apps",
	long_description=read_file("README.md"),
	long_description_content_type="text/markdown",
	author=__author__,
	author_email="cagdasbs@gmail.com",
	packages=find_packages("."),
	include_package_data=True,
	install_requires=read_requirements("requirements.txt"),
	classifiers=[
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Natural Language :: English",
		"License :: OSI Approved :: Apache Software License",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
	],
	license_files=("LICENSE",),
)
