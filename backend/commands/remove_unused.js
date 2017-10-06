var spawn = require('cross-spawn');

module.exports = (data, callback) => {
    var file_name = data.file_name;
    var proc = spawn('node_modules/.bin/tsc', [ file_name, '--noEmit', '--pretty', 'false', '--noUnusedLocals', '--allowJs'], { encoding: 'utf8' });
    proc.on('error', (err) => {
        callback(err);
    });
    stdout = '';
    proc.stdout.on('data', (d) => stdout += d);
    proc.on('exit', () => {
        var outlines = stdout.split('\n');
        var result = {};
        for (var i = 0; i < outlines.length; i++) {
            var line = outlines[i];
            var match = line.match(/^.+\((\d+),(\d+)\): error TS(\d+): '(\w+)'/);
            if (!match || match[3] !== '6133') continue;
            var line = Number(match[1]);
            var pos = Number(match[2]);
            var name = match[4];
            if (!Array.isArray(result[line])) {
                result[line] = [];
            }
            result[line].push({
                line: Number(match[1]),
                pos: Number(match[2]),
                name: match[4],
            });
        }
        callback(null, result);
    });
};