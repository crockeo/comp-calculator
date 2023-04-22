# comp-calculator

A quick little command-line tool for calculating
and comparing compensation packages.

## What?

Different companies provide different kinds of compensation packages.
It can be difficult to estimate how much net pay you'll actually receive
when taking into account:

- Cash compensation
- Equity compensation, like stock compensation vs. options compensation
- Pre-tax expenses, like contributing to healthcare and your 401k (with or without match?)

This tool provides a medium-accuracy estimate of your net income
taking all of those factors into account
so you can better compare different opportunities :)

## How?

```shell
git clone git@github.com:crockeo/comp-calculator
cd comp-calculator
python3.11 -m venv venv
. ./venv/bin/activate
pip install -r requirements3.txt
python main.py <path/to/config.yaml>
```

The repo also contains an [example configuration](./example_config.yaml)
which can be helpful when writing your own config.

```shell
# When running against the example config...
(venv) ~/src/personal/comp-calculator$ python main.py example_config.yaml
someplace
  gross taxable income  85000.00
  adjusted gross income 72674.52
  tax liability         10195.89
  net income            62478.63
tech_job
  gross taxable income  139250.00
  adjusted gross income 115424.52
  tax liability         20001.88
  net income            95422.64
```

## License

MIT Open Source Licensed. See [LICENSE](./LICENSE) file.
