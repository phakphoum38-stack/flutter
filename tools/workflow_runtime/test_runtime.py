import unittest

from .engine import WorkflowEngine
from .models import Job, JobState
from .queue import InMemoryQueue
from .runner import StatelessRunner


class WorkflowRuntimeTests(unittest.TestCase):
    def make_runtime(self):
        queue = InMemoryQueue()
        engine = WorkflowEngine(queue)
        runner = StatelessRunner(engine)
        return queue, engine, runner

    def test_successful_execution(self):
        _, engine, runner = self.make_runtime()
        engine.register_handler("echo", lambda payload: payload["value"])
        job = Job("j1", "w1", "echo", {"value": 42})

        engine.submit(job)
        result = runner.run_once()

        self.assertEqual(result.state, JobState.SUCCEEDED)
        self.assertEqual(result.output, 42)
        self.assertEqual(engine.state("j1"), JobState.SUCCEEDED)

    def test_failure_requeues_until_max_attempts(self):
        queue, engine, runner = self.make_runtime()
        engine.register_handler("broken", lambda _: (_ for _ in ()).throw(RuntimeError("boom")))
        job = Job("j2", "w1", "broken", max_attempts=2)

        engine.submit(job)
        first = runner.run_once()
        self.assertEqual(first.state, JobState.RETRY_WAIT)
        self.assertEqual(len(queue), 1)

        second = runner.run_once()
        self.assertEqual(second.state, JobState.FAILED)
        self.assertEqual(engine.state("j2"), JobState.FAILED)
        self.assertEqual(len(queue), 0)

    def test_duplicate_submission_is_rejected(self):
        queue, engine, _ = self.make_runtime()
        job = Job("j3", "w1", "echo")
        engine.submit(job)
        with self.assertRaises(ValueError):
            engine.submit(job)
        self.assertEqual(len(queue), 1)


if __name__ == "__main__":
    unittest.main()
