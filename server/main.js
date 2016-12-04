"use strict";

console.time("Server start time");

const net = require("net");
const _get = require("lodash.get");
const server_address = "127.0.0.1";
const server_port = process.argv[2];
const state = {
    packages: []
};

const commands = {
    ping: require('./commands/ping'),
    shutdown: require('./commands/shutdown'),
    read_packages: require('./commands/read_packages'),
    add_import_statement: require('./commands/add_import_statement'),
};

const server = net.createServer()
    .on("connection", socket => {
        socket.on("data", chunk => {
            try {
                var payload = JSON.parse(chunk.toString());    
            } catch (err) {
                return socket.emit("error", err);
            }
            console.log("Incoming message: %j", payload);
            payload._socket = socket;
            payload._server = server;
            payload._state = state;
            var cmd = _get(payload, "command");
            console.log("Command:", cmd);
            var func = _get(commands, cmd, (payload, callback) => callback());
            func(payload, (err, response) => {
                if (err) return socket.emit("error", err);
                console.log("Responding: %j", response);
                if (response) {
                    var responseJson = JSON.stringify(response);
                    socket.write(responseJson);
                }
                socket.end();
            });
        });
        socket.on("error", err => {
            console.error("Socket error", err);
            socket.write(err.toString());
        });
    })
    .on("error", err => {
        console.error("Server error", err.message);
    })
    .listen(server_port, server_address, () => {
        const addr = server.address();
        console.log("Listening: %s:%s (%s)", addr.address, addr.port, addr.family);
        console.timeEnd("Server start time");
    });
