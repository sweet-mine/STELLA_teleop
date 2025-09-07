from setuptools import find_packages
from setuptools import setup

package_name = 'wlkata_teleop_ros2'

setup(
    name=package_name,
    version='2.1.2',
    packages=find_packages(exclude=[]),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    author='ntrex',
    author_email='lab@ntrex.co.kr',
    maintainer='ntrex',
    maintainer_email='lab@ntrex.co.kr',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description=(
        'The wlkata_teleop package'
    ),
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'wlkata_teleop_key = wlkata_teleop_ros2.script.wlkata_teleop_key:main'
        ],
    },
)
