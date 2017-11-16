const esm = require('esm-exports');

module.exports = (data, callback) => {
    const folderList = data.folders || [];
    const result = [];
    const promises = folderList.map(d => esm.directory(d).then(items => {
        result.push(...items);
    }));
    return Promise.all(promises)
        .then(() => {
            callback(null, result);
        })
        .catch(err => {
            callback(err);
        });
};