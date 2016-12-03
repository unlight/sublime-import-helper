const tse = require("typescript-exports");
const _keys = require("lodash.keys");
const _flatten = require("lodash.flatten");
const readPkgUp = require("read-pkg-up");

module.exports = (payload, callback) => {
	var state = payload._state;
	var projectDirectory = payload.data.projectDirectory;
	Promise.all([
		tse.directory(projectDirectory),
		readPkgUp({
			cwd: projectDirectory,
			normalize: false
		})
		.then(p => [_keys(p.pkg.dependencies), _keys(p.pkg.devDependencies)])
		.then(dependencies => _flatten(dependencies))
		.then(names => Promise.all(names.map(n => tse.node(n, {
			baseDir: projectDirectory
		}))))
		.then(data => _flatten(data))
	])
	.then(results => {
		var [sources, modules] = results;
		return [].concat(sources, modules);
	})
	.then(results => {
		state.packages = results;
		callback(null, results);
	})
	.catch(err => callback(err))
};