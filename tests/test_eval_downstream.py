# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import importlib.resources

import kilt.eval_downstream
import kilt.eval_retrieval
import tests.test_data as test_data


def test_calculate_metrics():

    with importlib.resources.open_text(test_data, "gold1.jsonl") as gold_file:
        with importlib.resources.open_text(
            test_data, "guess1_1.jsonl"
        ) as guess_file:
            result = kilt.eval_downstream.evaluate(gold_file.name, guess_file.name)

            # kilt
            assert result["kilt"]["KILT-em"] == 1 / 3
            assert result["kilt"]["KILT-f1"] == 1 / 3
            assert result["kilt"]["KILT-rougel"] == 0.3333333316666667

            # downsream
            assert result["downstream"]["em"] == 2 / 3
            assert result["downstream"]["f1"] == 0.8333333333333334
            assert result["downstream"]["rougel"] == 0.7222222178240741

            # retrieval page level
            assert result["retrieval"]["Rprec"] == 1 / 3
            assert result["retrieval"]["recall@5"] == 1 / 3

        with importlib.resources.open_text(test_data, "gold1.jsonl") as guess_file:
            result = kilt.eval_downstream.evaluate(gold_file.name, guess_file.name)

            # kilt
            assert result["kilt"]["KILT-em"] == 1
            assert result["kilt"]["KILT-f1"] == 1
            assert result["kilt"]["KILT-rougel"] == 0.999999995

            # downsream
            assert result["downstream"]["em"] == 1
            assert result["downstream"]["f1"] == 1
            assert result["downstream"]["rougel"] == 0.999999995

            # retrieval page level
            assert result["retrieval"]["Rprec"] == 1
            assert result["retrieval"]["recall@5"] == 1

    with importlib.resources.open_text(test_data, "gold3.jsonl") as gold_file:
        with importlib.resources.open_text(
            test_data, "guess3_1.jsonl"
        ) as guess_file:

            result = kilt.eval_downstream.evaluate(gold_file.name, guess_file.name)

            # kilt
            assert result["kilt"]["KILT-em"] == 0
            assert result["kilt"]["KILT-f1"] == 0.25510204081632654
            assert result["kilt"]["KILT-rougel"] == 0.22352940932318338

            # downsream
            assert result["downstream"]["em"] == 0
            assert result["downstream"]["f1"] == 0.5102040816326531
            assert result["downstream"]["rougel"] == 0.44705881864636676
