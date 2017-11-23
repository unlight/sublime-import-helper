const esm = require('esm-exports');
const pick = require('1-liners/pick');
const readPkgUp = require('read-pkg-up');
const objectValues = require('object-values');

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
        .then(names => {
            const promises = names.map(n => esm.module(n, { basedir: importRoot }).then(items => {
                result.push(...items);
            }));
            return Promise.all(promises);
        })
        .then(() => {
            callback(null, result);
        })
        .catch(err => callback(err));
};