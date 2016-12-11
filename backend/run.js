var cmd = process.argv[2];
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
    shutdown: () => require('./commands/shutdown'),
    read_packages: () => require('./commands/read_packages'),
    insert_import_statement: () => require('./commands/insert_import_statement'),
    get_packages: () => require('./commands/get_packages'),
};

const runCommand = commands[cmd]();

runCommand(data, function(err, result) {
	if (err) {
		return console.error(err);
	}
	console.log(JSON.stringify(result));
});
