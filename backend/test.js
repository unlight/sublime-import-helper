import test from 'ava';
import * as Path from 'path';
const pkgDir = require('pkg-dir');
var rootPath;
var _state = { packages: [] };

test.before(() => {
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
var getPackagesCmd = require('./commands/get_packages');

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
        var [connection] = response.filter(item => item.name === 'connection');
        t.truthy(connection);
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

test.cb('Get packages no pkg', t => {
    var importRoot = Path.join(rootPath, 'test_playground/no_pkg');
    getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        t.falsy(err);
        t.truthy(response);
        t.truthy(response.length > 0);
        t.end();
    });
});

test.cb('Get packages with broken json', t => {
    var importRoot = Path.join(rootPath, 'test_playground/bad_json');
    getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        t.falsy(err);
        t.deepEqual(response, []);
        t.end();
    });
});

test.cb('Get packages with empty_pkg', t => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_pkg');
    getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        t.falsy(err);
        t.deepEqual(response, []);
        t.end();
    });
});

test.cb('Get packages with empty_file', t => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_file');
    getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        t.falsy(err);
        t.deepEqual(response, []);
        t.end();
    });
});