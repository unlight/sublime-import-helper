const esm = require('esm-exports');
const _keys = require('lodash/keys');
const _flatten = require('lodash/flatten');
const _get = require('lodash/get');
const _pick = require('lodash/pick');
const _merge = require('lodash/merge');
const _values = require('lodash/values');
const readPkgUp = require('read-pkg-up');

const emptyPkg = {
    dependencies: [],
    devDependencies: []
};

module.exports = (data, callback) => {
    var folderList = data.folders || [];
    var requests = folderList.map(d => esm.directory(d));
    var importRoot = data.importRoot;
    var packageKeys = data.packageKeys || ['dependencies', 'devDependencies'];
    if (importRoot) {
        var npmModules = readPkgUp({ cwd: importRoot, normalize: false })
            .catch(() => Promise.resolve(emptyPkg))
            .then(p => _get(p, 'pkg', emptyPkg))
            .then(pkg => _pick(pkg, packageKeys))
            .then(part => _keys(_merge(..._values(part))))
            .then(names => Promise.all(names.map(n => esm.parseModule(n, {dirname: importRoot}))))
            .then(data => _flatten(data));
        requests.push(npmModules);
    }
    Promise.all(requests)
        .then(results => _flatten(results))
        .then(results => callback(null, results))
        .catch(err => callback(err));
};
// 