const { esmExports } = require('esm-exports');

module.exports = (data, callback) => {
    const importRoot = data.importRoot;
    const name = data.name;
    if (!name) {
        callback(new Error('Expected non empty module name'));
        return;
    }

    return esmExports(name, { basedir: importRoot, type: 'module' })
        .then(items => {
            callback(null, items);
        })
        .catch(err => {
            if (!err) err = new Error('Unknow error.');
            callback(err);
        });
};