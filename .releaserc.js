module.exports = {
	plugins: [
		[
			'@semantic-release/exec',
			{
				prepareCmd: 'sh Taskfile prepare ${nextRelease.version}',
			},
		],
		'@semantic-release/commit-analyzer',
		'@semantic-release/release-notes-generator',
		'@semantic-release/changelog',
		'@semantic-release/github',
		[
			'@semantic-release/git',
			{
				assets: [
					'messages.json',
					'CHANGELOG.md',
					'package.json',
					'package-lock.json',
					'npm-shrinkwrap.json',
				],
			},
		],
	],
};
