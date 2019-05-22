const { esmExports } = require('esm-exports');
const fs = require('fs');

module.exports = (data, callback) => {
    const folders = data.folders || [];
    if (folders.length === 0 && data.importRoot) {
        folders.push(data.importRoot);
    }
    const result = [];
    const promises = folders
        .map(d => {
            if (fs.existsSync(d)) {
                return esmExports(d, { type: 'directory', ignorePatterns: (data.ignore || {})[d] })
                    .then(items => result.push(...items));
            }
        });

    return Promise.all(promises)
        .then(() => {
            callback(null, result);
        })
        .catch(err => {
            if (!err) err = new Error('Unknow error.');
            callback(err);
        });
};
