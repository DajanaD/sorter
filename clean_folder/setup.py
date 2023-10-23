from setuptools import setup, find_namespace_packages

setup(
      name='sort',
      version='1',
      url='https://github.com/DajanaD/sorter/tree/40b43583b24ace644a3a55a959532a85aa93ba8d/clean_folder',
      license='MIT',
      author='Diana',
      author_email='ccv080480@gmail.com',
      packages=find_namespace_packages(),
      install_requires=['markdown'],
      include_package_data=True,
      entry_points={'console_scripts': ['clean-folder=clean_folder.sort:run']},
)
