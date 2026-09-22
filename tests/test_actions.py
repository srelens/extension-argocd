"""Release manifests preserve the host's reviewed Argo CD action contract."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ActionTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / 'manifest.json').read_text())
        self.actions = {action['name']: action for action in self.manifest.get('actions', [])}

    def test_mutations_require_explicit_primitive_grants(self):
        self.assertEqual(set(self.actions), {'refresh', 'hard-refresh', 'sync'})
        self.assertTrue({'k8s.annotate', 'k8s.mergePatch'} <= set(self.manifest['permissions']))
        for action in self.actions.values():
            self.assertEqual(action['resource'], 'applications')
            self.assertIn(action['target'], self.manifest['permissions'])

    def test_sync_is_guarded_and_never_enables_pruning_or_replace(self):
        action = self.actions['sync']
        self.assertEqual(action['target'], 'k8s.mergePatch')
        operation = action['arguments']['patch']['operation']
        self.assertEqual(operation, {'initiatedBy': {'username': 'srelens'}, 'sync': {'prune': False, 'syncStrategy': {'hook': {}}}})
        self.assertEqual(action['preconditions'][0]['jsonPath'], '.operation')
        self.assertIs(action['preconditions'][0]['absent'], True)
        self.assertEqual(action['availableWhen'], action['preconditions'])

    def test_refresh_modes_are_explicit(self):
        for name, mode in [('refresh', 'normal'), ('hard-refresh', 'hard')]:
            self.assertEqual(self.actions[name]['arguments'], {'key': 'argocd.argoproj.io/refresh', 'value': mode})
