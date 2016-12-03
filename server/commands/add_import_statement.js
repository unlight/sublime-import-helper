const _filter = require('lodash.filter');

module.exports = (payload, callback) => {
	var identifier = payload.data;
	var packages = payload._state.packages;
	var result = [];
	if (identifier) {
		result = _filter(packages, item => identifier === item.name);
	}
	callback(null, result);
};