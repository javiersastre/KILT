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

    with importlib.resources.open_text(test_data, "gold2.jsonl") as gold_file:
        with importlib.resources.open_text(
            test_data, "guess2_1.jsonl"
        ) as guess_file:

            for rank_keys in [
                ["wikipedia_id"],
                ["wikipedia_id", "section"],
                ["wikipedia_id", "start_paragraph_id", "end_paragraph_id"],
            ]:

                result = kilt.eval_retrieval.evaluate(
                    gold_file.name, guess_file.name, ks=[1, 5], rank_keys=rank_keys,
                )
                assert result["Rprec"] == 1 / 2
                assert result["precision@1"] == 1
                assert result["precision@5"] == 2 / 5
                assert result["recall@5"] == 2 / 3
                assert result["success_rate@5"] == 1

        with importlib.resources.open_text(
            test_data, "guess2_2.jsonl"
        ) as guess_file:

            for rank_keys in [
                ["wikipedia_id"],
                ["wikipedia_id", "section"],
                ["wikipedia_id", "start_paragraph_id", "end_paragraph_id"],
            ]:

                result = kilt.eval_retrieval.evaluate(
                    gold_file.name, guess_file.name, ks=[1, 5], rank_keys=rank_keys,
                )
                assert result["Rprec"] == 1
                assert result["precision@1"] == 1
                assert result["precision@5"] == 1 / 5
                assert result["recall@5"] == 1 / 3
                assert result["success_rate@5"] == 1

