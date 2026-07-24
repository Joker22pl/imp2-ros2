from setuptools import setup
import os
from glob import glob

package_name = 'imp2_description'

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
        (os.path.join('share', package_name, 'config'),
            glob('config/*.yaml')),
        (os.path.join('share', package_name, 'urdf'),
            glob('urdf/*.xacro') if os.path.exists('urdf') else []),
        (os.path.join('share', package_name, 'rviz'),
            glob('rviz/*.rviz') if os.path.exists('rviz') else []),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Joker',
    maintainer_email='joker22pl@users.noreply.github.com',
    description='IMP2 robot: imp2_description',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
