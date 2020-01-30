import sys
import time
from functools import reduce
from pprint import pprint

from pycompss.api.task import task
from pycompss.api.api import compss_wait_on

from distributed_stats_model import Data, gen_random_data


def compute_stats(data):
    partition_stats = []
    for partition in data.split():
        partition_stats.append(_compute_stats(partition))
    # or partition_stats = list(map(lambda partition: _compute_stats(partition, column_name, column_type),
    #                               data.split()))

    final_stats = reduce(reduce_stats, partition_stats)
    final_stats = compss_wait_on(final_stats)
    return final_stats


@task(returns=dict)
def reduce_stats(stats, other_stats):
    reduced_stats = {}
    for column, column_stats in stats.items():
        reduced_stats[column] = {}
        for stat in column_stats:
            other_column_stats = other_stats[column]
            reduced_stats[column]["count"] = column_stats["count"] + other_column_stats["count"]
            if stat == "max_len":
                reduced_stats[column]["max_len"] = max(column_stats["max_len"], other_column_stats["max_len"])
            elif stat == "min_len":
                reduced_stats[column]["min_len"] = min(column_stats["min_len"], other_column_stats["min_len"])
            elif stat == "empty_values":
                reduced_stats[column]["empty_values"] = column_stats["empty_values"] + other_column_stats[
                    "empty_values"]
            elif stat == "max":
                reduced_stats[column]["max"] = max(column_stats["max"], other_column_stats["max"])
            elif stat == "min":
                reduced_stats[column]["min"] = min(column_stats["min"], other_column_stats["min"])
            elif stat == "mean":
                avg_mean = (column_stats["count"] * column_stats["mean"] + other_column_stats["count"] *
                            other_column_stats["mean"]) / reduced_stats[column]["count"]
                reduced_stats[column]["mean"] = avg_mean
            elif stat == "false":
                reduced_stats[column]["false"] = column_stats["false"] + other_column_stats["false"]
            elif stat == "true":
                reduced_stats[column]["true"] = column_stats["true"] + other_column_stats["true"]

    return reduced_stats


@task(returns=dict)
def _compute_stats(partition):
    val1_stats = {
        "count": 0,
        "max_len": float("-inf"),
        "min_len": float("inf"),
        "empty_values": 0
    }
    val2_stats = {
        "sum": 0,
        "count": 0,
        "mean": 0,
        "max": float("-inf"),
        "min": float("inf"),
    }
    val3_stats = {
        "count": 0,
        "false": 0,
        "true": 0
    }
    for row_values in partition.values():
        val1 = row_values.val1
        val1_stats["count"] += 1
        val1_stats["max_len"] = max(val1_stats["max_len"], len(val1))
        if len(val1) == 0:
            val1_stats["empty_values"] += 1
        else:
            val1_stats["min_len"] = min(val1_stats["min_len"], len(val1))

        val2 = row_values.val2
        val2_stats["count"] += 1
        val2_stats["max"] = max(val2_stats["max"], val2)
        val2_stats["min"] = min(val2_stats["min"], val2)
        val2_stats["sum"] += val2

        val3 = row_values.val3
        val3_stats["count"] += 1
        if val3:
            val3_stats["true"] += 1
        else:
            val3_stats["false"] += 1

    val2_stats["mean"] = val2_stats["sum"] / val2_stats["count"]

    stats = {
        "val1": val1_stats,
        "val2": val2_stats,
        "val3": val3_stats
    }

    return stats


def main():
    data = Data("my_app.data")

    try:
        gen_data = bool(sys.argv[1])
    except IndexError:
        gen_data = True

    if gen_data:
        gen_random_data("my_app.data", rows=1000)
        time.sleep(2)

    stats = compute_stats(data)
    print("\n")
    pprint(stats)
    print("\n")


if __name__ == "__main__":
    main()
