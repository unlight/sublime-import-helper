const esm = require('esm-exports');
const _keys = require('lodash.keys');
const _flatten = require('lodash.flatten');
const _get = require('lodash.get');
const readPkgUp = require('read-pkg-up');

const emptyPkg = {
    dependencies: [],
    devDependencies: []
};

module.exports = (data, callback) => {
    var folderList = data.folders || [];
    var requests = folderList.map(d => esm.directory(d));
    var importRoot = data.importRoot;
    if (importRoot) {
        var npmModules = readPkgUp({ cwd: importRoot, normalize: false })
            .catch(() => Promise.resolve(emptyPkg))
            .then(p => _get(p, 'pkg', emptyPkg))
            .then(p => [_keys(p.dependencies), _keys(p.devDependencies)])
            .then(dependencies => _flatten(dependencies))
            .then(names => Promise.all(names.map(n => esm.parseModule(n, {dirname: importRoot}))))
            .then(data => _flatten(data));
        requests.push(npmModules);
    }
    Promise.all(requests)
        .then(results => _flatten(results))
        .then(results => callback(null, results))
        .catch(err => callback(err));
};