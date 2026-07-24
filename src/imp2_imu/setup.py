from setuptools import setup
import os
from glob import glob

package_name = 'imp2_imu'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joker',
    maintainer_email='joker22pl@users.noreply.github.com',
    description='BNO085 IMU driver for IMP2 robot',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imp2_imu_node = imp2_imu.imp2_imu_node:main',
        ],
    },
)
