const esm = require('esm-exports');
const pick = require('1-liners/pick');
const readPkgUp = require('read-pkg-up');
const objectValues = require('object-values');

const emptyPkg = {
    dependencies: [],
    devDependencies: []
};

module.exports = (data, callback) => {
    const folderList = data.folders || [];
    const result = [];
    const promises = folderList.map(d => esm.directory(d).then(items => {
        result.push(...items);
    });
    Promise.all(requests)
        .then(() => {
            callback(null, result);
        })
        .catch(err => {
            callback(err);
        });
};