from setuptools import setup

kwargs = {
    'name': 'django-xadditions',
    'version': '0.1.5',
    'description': 'Common django additions.',
    'author': 'Tartnskyi Vladimir',
    'author_email': 'fon.vosi@gmail.com',
    'url': 'https://github.com/vosi/django-xadditions',
    'keywords': 'django,snippets',
    'license': 'BSD',
    'packages': ['xadditions',],
    'include_package_data': True,
    'install_requires': ['setuptools'],
    'zip_safe': False,
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ],
}
setup(**kwargs)
