const { esmExports } = require('esm-exports');
const pick = require('1-liners/pick');
const readPkgUp = require('read-pkg-up');
const objectValues = require('object-values');

// Deprecated, use get_modules and get_folders instead.

const emptyPkg = {
    dependencies: [],
    devDependencies: []
};

module.exports = (data, callback) => {
    const folderList = data.folders || [];
    const result = [];
    const requests = folderList.map(d => esmExports(d, { type: 'directory' }).then(items => {
        result.push(...items);
    }));
    const importRoot = data.importRoot;
    const packageKeys = data.packageKeys || ['dependencies', 'devDependencies'];
    if (importRoot) {
        const npmModules = readPkgUp({ cwd: importRoot, normalize: false })
            .catch(() => Promise.resolve(emptyPkg))
            .then(p => p && p.pkg || emptyPkg)
            .then(pkg => pick(packageKeys, pkg))
            .then(part => {
                const values = Object.assign({}, ...objectValues(part));
                return Object.keys(values);
            })
            .then(names => {
                const promises = names.map(n => esmExports(n, { dirname: importRoot, type: 'module' }).then(items => {
                    result.push(...items);
                }));
                return Promise.all(promises);
            });
        requests.push(npmModules);
    }
    return Promise.all(requests)
        .then(() => {
            callback(null, result);
        })
        .catch(err => callback(err));
};