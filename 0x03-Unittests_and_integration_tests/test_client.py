#!/usr/bin/env python3
"""A test module for utils module
"""
import unittest
from unittest.mock import PropertyMock, patch

from parameterized import parameterized

GithubOrgClient = __import__('client').GithubOrgClient


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
