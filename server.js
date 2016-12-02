"use strict";

const net = require("net");
const child_process = require("child_process");
const path = require("path");
const tse = require("typescript-exports");
const readPkgUp = require("read-pkg-up");
const _ = require("lodash");

const server_address = process.argv[2] || "127.0.0.1";
const server_port = process.argv[3];

const server = net.createServer()
    .on("connection", socket => {
        socket.on("data", chunk => {
            try {
                var payload = JSON.parse(chunk.toString());    
            } catch (err) {
                return socket.emit("error", err);
            }
            console.log("Incoming message: %j", payload);
            payload.socket = socket;
            payload.server = server;
            var cmd = _.get(payload, "command");
            console.log("Command: " + cmd);
            var func = _.get(commands, cmd, (payload, callback) => callback());
            func(payload, (err, response) => {
                if (err) return socket.emit("error", err);
                if (response) {
                    response = JSON.stringify(response, null, 1);
                    console.log("Responding: %s", response);
                    socket.write(response);
                }
                socket.end();
            });
        });
        socket.on("error", err => {
            console.log("Socket error", err);
            socket.write(err.toString());
        });
    })
    .on("error", err => {
        console.error("Server error", err.message);
    })
    .listen(server_port, server_address, (err) => {
        const addr = server.address();
        console.log("Listening: %s:%s (%s)", addr.address, addr.port, addr.family);
    });

var packages = [];
const commands = {
    ping: (payload, callback) => {
        setTimeout(() => {
            var response = "Pong: " + new Date();
            callback(null, response);
        }, 1000);
    },
    echo: (payload, callback) => {
        var data = _.get(payload, "data", "No data");
        callback(null, data);
    },
    setup: (payload, callback) => {
        var options = {cwd: __dirname};
        var cmd = "npm i";
        child_process.exec(cmd, options, (error, stdout, stderr) => {
            if (error) return callback(error);
            callback(null, stdout);
        });
    },
    shutdown: (data, callback) => {
        var server = data.server;
        server.close();
        callback();
    },
    read_packages: (payload, callback) => {
        var projectDirectory = payload.data.projectDirectory;
        Promise.all([
            tse.directory(projectDirectory),
            readPkgUp({cwd: projectDirectory, normalize: false})
                .then(p => [_.keys(p.pkg.dependencies), _.keys(p.pkg.devDependencies)])
                .then(dependencies => _.flatten(dependencies))
                .then(names => Promise.all(names.map(n => tse.node(n, {baseDir: projectDirectory}))))
                .then(data => _.flatten(data))
        ]).then(results => {
            var [sources, modules] = results;
            return [].concat(sources, modules);
        }).then(results => {
            packages = results;
            callback(null, results);
        }).catch(err => callback(err))
    },
    add_import_statement: (payload, callback) => {
        var identifier = payload.data;
        var result = [];
        if (identifier) {
            result = _.filter(packages, item => identifier === item.name);
        }
        callback(null, result);
    },
};
