import glob
import os
from setuptools import setup
package_name = 'jumpbot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/'+package_name+'/launch',glob.glob(os.path.join('launch','*.launch.py'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='mosiwon',
    maintainer_email='mosiwon@todo.todo',
    description='TODO: Package description',
    license='TODO: License dec laration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'self_balancing = jumpbot.self_balancing:main',
            'param_pid_node = jumpbot.param_pid_node:main',
            'pidcontrol = jumpbot.pidcontrol:main',
            'SelfBalance = jumpbot.SelfBalance:main',  
        ],
    },
)
