'use strict';
const assert = require('assert');
const Path = require('path');
const pkgDir = require('pkg-dir');
var rootPath;
const _state = { packages: [] };

const getPackagesCmd = require('./commands/get_packages');
const ping = require('./commands/ping');

it('smoke test', () => {
    assert(true);
});

beforeEach(() => {
    return pkgDir(__dirname).then(value => {
        rootPath = value;
    });    
});
    
it('Ping', done => {
    ping({}, (err, response) => {
        if (err) throw err;
        assert(response.message === 'Pong');
        assert(response.date);
        done();
    });
});

it('Get packages', () => {
    var importRoot = Path.join(rootPath, 'test_playground');
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert(response);
        assert(response.length > 0);
    });
});

it('Get packages no pkg', () => {
    var importRoot = Path.join(rootPath, 'test_playground/no_pkg');
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert(response);
        assert(response.length > 0);
    });
});

it('Get packages with broken json', () => {
    var importRoot = Path.join(rootPath, 'test_playground/bad_json');
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('Get packages with empty_pkg', () => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_pkg');
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('Get packages with empty_file', () => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_file');
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('Get packages for root (no package found)', () => {
    var importRoot = '/';
    return getPackagesCmd({
        _state: _state,
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});
