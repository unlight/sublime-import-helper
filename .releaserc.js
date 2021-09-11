module.exports = {
    plugins: [
        [
            '@semantic-release/commit-analyzer',
            {
                preset: 'conventionalcommits',
            },
        ],
        [
            '@semantic-release/release-notes-generator',
            {
                preset: 'conventionalcommits',
            },
        ],
        [
            '@semantic-release/exec',
            {
                prepareCmd: 'sh Taskfile prepare ${nextRelease.version}',
            },
        ],
        '@semantic-release/changelog',
        '@semantic-release/github',
        [
            '@semantic-release/git',
            {
                assets: ['messages.json', 'CHANGELOG.md'],
            },
        ],
    ],
};
