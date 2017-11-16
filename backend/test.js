'use strict';
const assert = require('assert');
const Path = require('path');
const pkgDir = require('pkg-dir');
const _state = { packages: [] };

const getPackagesCmd = require('./commands/get_packages');
const getFoldersCmd = require('./commands/get_folders');
const ping = require('./commands/ping');

const rootPath = pkgDir.sync(__dirname);

it('smoke test', () => {
    assert(true);
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

it('Get packages source only (ignore node_modules)', () => {
    return getPackagesCmd({
        _state: _state,
        folders: [rootPath],
        packageKeys: [],
    }, (err, response) => {
        assert.ifError(err);
        assert(response);
        assert(response.length);
        let [greeter] = response.filter(x => x.name === 'Greeter');
        assert(greeter);
    });
});

it('get_folders command', (done) => {
    const folder1 = Path.join(rootPath, 'test_playground/component');
    const folder2 = Path.join(rootPath, 'test_playground/lib');
    getFoldersCmd({
        folders: [folder1, folder2],
    }, (err, result) => {
        if (err) return done(err);
        assert(result.find(m => m.name === 'Animal'));
        assert(result.find(m => m.name === 'AbcComponent'));
        assert(result.filter(m => m.name === 'x2').length > 1);
        done();
    });
});