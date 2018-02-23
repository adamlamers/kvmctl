from setuptools import setup, find_packages

setup(
        name='kvmctl',
        version='0.1',
        description='kvm/libvirt CLI Utilities',
        url='',
        author='Adam Lamers',
        author_email='adamlamers@gmail.com',
        install_requires = ['click',
            'libvirt-python'],
        packages=['kvmctl'],
        entry_points={
            'console_scripts': [
                    'kvmctl=kvmctl.__main__:cli'
                ]
            },
        include_package_data=True

)
