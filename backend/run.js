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
	remove_unused: () => require('./commands/remove_unused'),
	get_folders: () => require('./commands/get_folders'),
	get_module: () => require('./commands/get_module'),
	get_from_package: () => require('./commands/get_from_package'),
};

const runCommand = commands[cmd]();

runCommand(data, function(err, result) {
	if (err) {
		return console.error(err);
	}
	console.log(JSON.stringify(result));
});
