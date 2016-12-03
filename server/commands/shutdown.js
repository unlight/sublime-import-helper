module.exports = (data, callback) => {
	var server = data._server;
	server.close();
	callback();
};