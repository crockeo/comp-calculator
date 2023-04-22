#!/usr/bin/env python3
import argparse
import dataclasses
from os import name
import sys
from pathlib import Path
from typing import Any

import yaml


def main(raw_args: list[str]) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    args = parser.parse_args(raw_args[1:])

    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = Path.cwd() / config_path
    config_path = config_path.resolve()

    with open(config_path) as f:
        config = yaml.safe_load(f)

    for job in config["jobs"]:
        income = net_income(job, config["tax_brackets"])
        income.render()


@dataclasses.dataclass
class Income:
    job: str
    gross_taxable_income: float
    adjusted_gross_income: float
    tax_liability: float
    net_income: float

    def render(self) -> None:
        print(self.job)
        print(f"  gross taxable income  {self.gross_taxable_income:.2f}")
        print(f"  adjusted gross income {self.adjusted_gross_income:.2f}")
        print(f"  tax liability         {self.tax_liability:.2f}")
        print(f"  net income            {self.net_income:.2f}")


def net_income(job: dict[str, Any], tax_brackets: list[dict[str, Any]]) -> Income:
    gross_taxable_income = 0
    for taxable_income in job["taxable_income"]:
        gross_taxable_income += taxable_income_amount(taxable_income)

    adjusted_gross_income = gross_taxable_income
    for pretax_expense in job["pretax_expense"]:
        adjusted_gross_income -= pretax_expense["amount"]

    tax_liability = calculate_tax_liability(adjusted_gross_income, tax_brackets)
    return Income(
        job=job["name"],
        gross_taxable_income=gross_taxable_income,
        adjusted_gross_income=adjusted_gross_income,
        tax_liability=tax_liability,
        net_income=adjusted_gross_income - tax_liability,
    )


def taxable_income_amount(taxable_income: dict[str, Any]) -> float:
    if cash_value := taxable_income.get("cash_value"):
        return cash_value

    if taxable_income["name"] == "options":
        # From: https://www.schwab.com/learn/story/how-are-options-taxed
        #
        # > Generally, the gains from exercising non-qualified stock options
        # > are treated as ordinary income, whereas gains from an incentive stock option
        # > can be either treated as ordinary income
        # > or can be taxed at a preferential rate,
        # > if certain requirements are met.
        #
        # TL;DR:
        amount_per_year = taxable_income["total"] / taxable_income.get("years", 1)
        market_price = amount_per_year * taxable_income["last_preferred_price"]
        exercise_cost = amount_per_year * taxable_income["strike_price"]
        return market_price - exercise_cost

    raise ValueError(f"cannot calculate taxable income amount from {taxable_income}")


def calculate_tax_liability(adjusted_gross_income: float, tax_brackets: list[dict[str, Any]]) -> float:
    tax_liability = 0
    for tax_bracket in tax_brackets:
        lower = tax_bracket["min"]
        upper = tax_bracket.get("max")
        rate = tax_bracket["rate"]

        if upper is not None and adjusted_gross_income > upper:
            tax_liability += (upper - lower) * rate
        elif (
            adjusted_gross_income > lower
            and (
                upper is None
                or adjusted_gross_income < upper
            )
        ):
            tax_liability += (adjusted_gross_income - lower) * rate
    return tax_liability


if __name__ == "__main__":
    main(sys.argv)
