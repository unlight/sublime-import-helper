'use strict';
const assert = require('assert');
const Path = require('path');
const pkgDir = require('pkg-dir');

const getFoldersCmd = require('./commands/get_folders');
const getModulesCmd = require('./commands/get_modules');
const ping = require('./commands/ping');

const rootPath = pkgDir.sync(__dirname);

it('smoke test', () => {
    assert(true);
});

it('ping', done => {
    ping({}, (err, response) => {
        if (err) throw err;
        assert(response.message === 'Pong');
        assert(response.date);
        done();
    });
});

it('get folders importRoot will bed added if not folders', () => {
    var importRoot = Path.join(rootPath, 'test_playground');
    return getFoldersCmd({
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert(response);
        assert(response.length > 0);
    });
});

it('get folders no pkg', () => {
    var importRoot = Path.join(rootPath, 'test_playground/no_pkg');
    return getFoldersCmd({
        folders: [],
        importRoot: importRoot,
    }, (err, result) => {
        assert.ifError(err);
        assert.deepEqual(result, []);
    });
});

it('get packages with broken json', () => {
    var importRoot = Path.join(rootPath, 'test_playground/bad_json');
    return getFoldersCmd({
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('get packages with empty_pkg', () => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_pkg');
    return getFoldersCmd({
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('get packages with empty_file', () => {
    var importRoot = Path.join(rootPath, 'test_playground/empty_file');
    return getFoldersCmd({
        folders: [],
        importRoot: importRoot
    }, (err, response) => {
        assert.ifError(err);
        assert.deepEqual(response, []);
    });
});

it('get packages source only (ignore node_modules)', () => {
    return getFoldersCmd({
        folders: [rootPath],
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

it('get_modules command', (done) => {
    getModulesCmd({

    }, (err, result) => {
        if (err) return done(err);
        assert(result.find(m => m.name === 'parse')); // esm-exports
        assert(result.find(m => m.name === 'directory'));
        assert(result.find(m => m.name === 'Component')); // @angular/core
        assert(result.find(m => m.name === 'inject')); // @angular/core/testing
        done();
    });
});

it('get only dependencies', () => {
    getModulesCmd({
        packageKeys: ['dependencies'],
    }, (err, result) => {
        assert.ifError(err);
        assert.deepEqual(result, []);
    });
});

it('get folders error', () => {
    return getFoldersCmd({
        folders: null,
        importRoot: 'foobar',
    }, (err, response) => {
        assert(err);
        assert.ifError(response);
    });
});

describe('if error undefined we should set it to unknown err', () => {
    
    before(() => {
        const esm = require('esm-exports');
        esm.module = () => Promise.reject(undefined);
        esm.directory = () => Promise.reject(undefined);
    });

    after(() => {
        delete require.cache[require.resolve('esm-exports')];
    });

    it('get modules', () => {
        return getModulesCmd({
        }, (err) => {
            assert(err);
        });
    });

    it('get folders', () => {
        return getFoldersCmd({
            folders: [],
            importRoot: Path.join(rootPath, 'test_playground')
        }, (err, response) => {
            assert(err);
        });
    });
});

