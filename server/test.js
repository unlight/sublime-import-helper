import test from 'ava';
const pkgDir = require('pkg-dir');
var rootPath;
var _state = { packages: [] };

test.before(t => {
    return pkgDir(__dirname).then(value => {
        rootPath = value;
    });
});

test.cb('Ping', t => {
    var ping = require('./commands/ping');
    ping({}, (err, response) => {
        if (err) throw err;
        t.is(response.message, 'Pong');
        t.truthy(response.date);
        t.end();
    });
});

var readPackagesCmd = require('./commands/read_packages');

test.cb('Read packages', t => {
    var projectDirectory = rootPath;
    readPackagesCmd({
        _state: _state,
        data: { projectDirectory }
    }, (err, response) => {
        if (err) throw err;
        t.truthy(Array.isArray(response));
        var emptyItems = response.filter(v => !v);
        t.truthy(emptyItems.length === 0);
        t.end();
    });
});

test.cb('Read packages projectDirectory null', t => {
    readPackagesCmd({
        _state: _state,
        data: {
            projectDirectory: null
        }
    }, (err, response) => {
        t.truthy(err);
        t.falsy(response);
        t.end();
    });
});