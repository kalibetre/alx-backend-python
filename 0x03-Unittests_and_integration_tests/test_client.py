#!/usr/bin/env python3
"""A test module for utils module
"""
import unittest
from unittest.mock import MagicMock, PropertyMock, patch

from parameterized import parameterized, parameterized_class

GithubOrgClient = __import__('client').GithubOrgClient
TEST_PAYLOAD = __import__('fixtures').TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class
    """

    @parameterized.expand(['google', 'abc'])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method
        """
        mock_get_json.return_value = {'payload': True}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, mock_get_json.return_value)
        mock_get_json.assert_called_once()

    def test_public_repos_url(self):
        """Test the _public_repos_url property
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            expected = {"repos_url": 'GithubOrgClient.org'}
            mock_org.return_value = expected
            client = GithubOrgClient(expected)
            self.assertEqual(client._public_repos_url, expected['repos_url'])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method
        """
        mock_get_json.return_value = [{
            "name": "episodes.dart"
        }, {
            "name": "cpp-netlib"
        }]
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = 'google/repos'
            client = GithubOrgClient('')
            self.assertEqual(client.public_repos(),
                             ["episodes.dart", "cpp-netlib"])
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({
            "license": {
                "key": "my_license"
            }
        }, "my_license", True),
        ({
            "license": {
                "key": "other_license"
            }
        }, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    TEST_PAYLOAD,
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient class
    """

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class
        """
        cls.get_patcher = patch('requests.get', new=MagicMock())
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.return_value = cls.org_payload

    @classmethod
    def tearDownClass(cls):
        """Tear down class
        """
        cls.get_patcher.stop()

    def test_requests_get_with_side_effect(self):
        """Test requests.get with side_effect
        """
        self.mock_get.return_value.json.side_effect = [
            self.org_payload,
            self.repos_payload,
        ]
        client = GithubOrgClient('google')
        org = client.org
        repos = client.public_repos()

        self.assertEqual(org, self.org_payload)
        self.assertEqual(repos, self.expected_repos)
