import unittest
import json
import tempfile
from pathlib import Path


class RelationDialogueSmokeTests(unittest.TestCase):
    def test_twenty_round_smoke_report_flags_empty_forbidden_and_duplicate_output(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            build_relation_dialogue_smoke_report,
            generate_unique_relation_smoke_prompt_set,
        )

        prompts = generate_unique_relation_smoke_prompt_set(
            run_seed="report-fixture"
        )["prompts"]
        responses = [
            "第一轮自然回应",
            "",
            "这里不应该出现用户这个关系词",
            "重复回应",
            "重复回应",
        ] + [f"自然回应 {index}" for index in range(6, 21)]

        report = build_relation_dialogue_smoke_report(
            prompts=prompts,
            responses=responses,
        )

        self.assertEqual(report["schema_version"], "relation_dialogue_smoke_report_v0")
        self.assertEqual(report["required_round_count"], 20)
        self.assertEqual(report["actual_round_count"], 20)
        self.assertTrue(report["prompt_uniqueness"]["unique"])
        self.assertEqual(report["natural_language_release_count"], 19)
        self.assertEqual(report["empty_response_rounds"], [2])
        self.assertEqual(report["duplicate_response_rounds"], [5])
        self.assertEqual(
            report["forbidden_surface_hits"],
            [{"round": 3, "term": "用户"}],
        )
        self.assertEqual(report["completion_status"], "failed")

    def test_unreleased_adam_json_stdout_is_not_counted_as_spoken_response(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            extract_adam_response_text,
        )

        response_text, parsed = extract_adam_response_text(
            """
            {
              "schema_version": "resident_relation_send_result_v0",
              "send_status": "completed",
              "response_status": "completed_unreleased",
              "natural_language_released": false,
              "resident_relation_outbox_ref": "runtime/state/terminal/resident_relation_outbox.jsonl"
            }
            """
        )

        self.assertEqual(response_text, "")
        self.assertEqual(parsed["response_status"], "completed_unreleased")
        self.assertIs(parsed["natural_language_released"], False)

    def test_model_channel_preflight_blocks_invalid_token_before_twenty_rounds(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            build_model_channel_preflight_report,
        )

        report = build_model_channel_preflight_report(
            model_provider="openai-compatible",
            model_name="gpt-5.5",
            model_base_url="https://example.invalid/v1",
            model_api_key_present=True,
            models=[],
            models_error='http_401: {"message":"Invalid token"}',
            chat_response_text="",
            chat_error='http_401: {"message":"Invalid token"}',
        )

        self.assertEqual(report["schema_version"], "model_channel_preflight_v0")
        self.assertFalse(report["ready_for_dialogue_smoke"])
        self.assertEqual(report["models_endpoint_status"], "failed")
        self.assertEqual(report["chat_completion_status"], "failed")
        self.assertIn("invalid_token", report["failure_reasons"])

    def test_smoke_runner_does_not_call_adam_when_preflight_fails(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            run_adam_relation_dialogue_smoke,
        )

        calls = []

        def fake_run(*args, **kwargs):
            calls.append((args, kwargs))
            raise AssertionError("Adam should not be called when preflight fails")

        report = run_adam_relation_dialogue_smoke(
            prompt_generation_seed="preflight-blocked-fixture",
            preflight_report={
                "schema_version": "model_channel_preflight_v0",
                "ready_for_dialogue_smoke": False,
                "failure_reasons": ["invalid_token"],
            },
            subprocess_run=fake_run,
        )

        self.assertEqual(calls, [])
        self.assertEqual(report["completion_status"], "failed")
        self.assertEqual(report["actual_round_count"], 0)
        self.assertEqual(report["planned_round_count"], 20)
        self.assertEqual(report["preflight"]["failure_reasons"], ["invalid_token"])
        self.assertEqual(
            report["prompt_generation"]["prompt_generation"],
            "runtime_seeded_unique_mix",
        )

    def test_loads_unique_prompt_set_file_and_records_prompt_set_identity(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            load_prompt_set_file,
            run_adam_relation_dialogue_smoke,
        )

        prompts = [f"唯一验收问题 {index}" for index in range(1, 21)]
        with tempfile.TemporaryDirectory() as tmp:
            prompt_file = Path(tmp) / "unique_prompts.json"
            prompt_file.write_text(
                json.dumps(
                    {
                        "prompt_set_id": "it10-unique-smoke-001",
                        "prompts": prompts,
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            loaded = load_prompt_set_file(prompt_file)

        self.assertEqual(loaded["prompt_set_id"], "it10-unique-smoke-001")
        self.assertEqual(loaded["prompts"], prompts)

        def fake_run(args, **kwargs):
            round_number = prompts.index(args[2]) + 1
            return type(
                "Completed",
                (),
                {
                    "returncode": 0,
                    "stdout": f"自然释放 {round_number}",
                    "stderr": "",
                },
            )()

        report = run_adam_relation_dialogue_smoke(
            prompts=loaded["prompts"],
            prompt_set_id=loaded["prompt_set_id"],
            preflight_report={"ready_for_dialogue_smoke": True},
            subprocess_run=fake_run,
        )

        self.assertEqual(report["completion_status"], "passed")
        self.assertEqual(report["prompt_set_id"], "it10-unique-smoke-001")
        self.assertEqual(len(report["prompt_sha256s"]), 20)
        self.assertEqual(len(set(report["prompt_sha256s"])), 20)

    def test_default_smoke_prompts_are_generated_per_run_not_static(self):
        from life_v0.process_supervisor.relation_dialogue_smoke import (
            generate_unique_relation_smoke_prompt_set,
            run_adam_relation_dialogue_smoke,
        )

        first = generate_unique_relation_smoke_prompt_set(run_seed="run-a")
        second = generate_unique_relation_smoke_prompt_set(run_seed="run-b")

        self.assertEqual(len(first["prompts"]), 20)
        self.assertEqual(len(set(first["prompts"])), 20)
        self.assertEqual(len(second["prompts"]), 20)
        self.assertEqual(len(set(second["prompts"])), 20)
        self.assertNotEqual(first["prompt_set_id"], second["prompt_set_id"])
        self.assertNotEqual(first["prompts"], second["prompts"])

        calls = []

        def fake_run(args, **kwargs):
            calls.append(args)
            return type(
                "Completed",
                (),
                {
                    "returncode": 0,
                    "stdout": json.dumps(
                        {
                            "response_text": f"自然释放 {len(calls)}",
                            "natural_language_released": True,
                        },
                        ensure_ascii=False,
                    ),
                    "stderr": "",
                },
            )()

        report = run_adam_relation_dialogue_smoke(
            prompt_generation_seed="run-default",
            preflight_report={"ready_for_dialogue_smoke": True},
            subprocess_run=fake_run,
        )

        self.assertEqual(report["completion_status"], "passed")
        self.assertEqual(report["actual_round_count"], 20)
        self.assertEqual(len(calls), 20)
        self.assertEqual(len(set(report["prompt_sha256s"])), 20)
        self.assertEqual(
            report["prompt_generation"]["prompt_generation"],
            "runtime_seeded_unique_mix",
        )


if __name__ == "__main__":
    unittest.main()
