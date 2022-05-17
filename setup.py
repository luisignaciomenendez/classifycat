from setuptools import setup

setup(
    name="catalan-classifier",
    version='0.1',
    py_modules=['classify'],
    author='Luis I. Menéndez | luisigmenendez@gmail.com',
    install_requires=[
        'Click',
        'pandas',
    ],
    # entry_points='''
    #     [console_scripts]
    #     classify=classify:cli
    #     retrain=retrain:cli
    # ''',
    entry_points={
            "console_scripts": [
                "classifycat = catalan-classifier.command:classifycat",
            ]
        },
)
