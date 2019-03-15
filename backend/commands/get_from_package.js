const readPkgUp = require('read-pkg-up');
const objectValues = require('object-values');
const pick = require('1-liners/pick');

const emptyPkg = {
    dependencies: [],
    devDependencies: [],
};

module.exports = (data, callback) => {
    const result = [];
    const importRoot = data.importRoot;
    const packageKeys = data.packageKeys || ['dependencies', 'devDependencies'];
    return readPkgUp({ cwd: importRoot, normalize: false })
        .catch(() => Promise.resolve(emptyPkg))
        .then(p => p && p.pkg || emptyPkg)
        .then(pkg => pick(packageKeys, pkg))
        .then(part => {
            const values = Object.assign({}, ...objectValues(part));
            return Object.keys(values);
        })
        .then(result => {
            callback(null, result);
        })
        .catch(err => {
            if (!err) {
                err = new Error('Unknow error');
            }
            callback(err);
        });
};