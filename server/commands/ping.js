module.exports = (payload, callback) => {
	setTimeout(() => {
		var response = {message: "Pong", date: new Date()};
		callback(null, response);
	}, 500);
};