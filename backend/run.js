const cmd = process.argv[2];
var data = process.argv[3];

if (data) {
	try {
		data = JSON.parse(data);
	} catch (e) {
		console.error(e);
		process.exit();
	}
}

const commands = {
	ping: () => require('./commands/ping'),
	get_packages: () => require('./commands/get_packages')
};

const runCommand = commands[cmd]();

runCommand(data, function(err, result) {
	if (err) {
		return console.error(err);
	}
	console.log(JSON.stringify(result));
});

