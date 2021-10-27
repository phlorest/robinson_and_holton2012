from setuptools import setup


setup(
    name='cldfbench_robinson_and_holton2012',
    py_modules=['cldfbench_robinson_and_holton2012'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'cldfbench.dataset': [
            'robinson_and_holton2012=cldfbench_robinson_and_holton2012:Dataset',
        ]
    },
    install_requires=[
        'phlorest',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
