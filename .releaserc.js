module.exports = {
	branches: [
		{ name: 'master' },
		{ name: 'next', channel: 'next' }, // Only after the `next` is created in the repo
	],
	plugins: [
		'@semantic-release/commit-analyzer',
		'@semantic-release/release-notes-generator',
		'@semantic-release/changelog',
		'@semantic-release/github',
		'@semantic-release/git',
	],
};
