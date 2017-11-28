const esm = require('esm-exports');

module.exports = (data, callback) => {
    const folders = data.folders || [];
    if (folders.length === 0 && data.importRoot) {
        folders.push(data.importRoot);
    }
    const result = [];
    const promises = folders.map(d => esm.directory(d).then(items => {
        result.push(...items);
    }));
    return Promise.all(promises)
        .then(() => {
            callback(null, result);
        })
        .catch(err => {
            if (!err) err = new Error('Unknow error.');
            callback(err);
        });
};