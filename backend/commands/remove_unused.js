var spawn = require('cross-spawn');

module.exports = (data, callback) => {
    var file_name = data.file_name.replace(/\\/g, '/');
    var options = { encoding: 'utf8' , cwd: data.cwd };
    var proc = spawn('node_modules/.bin/tsc', [file_name, '--noEmit', '--pretty', 'false', '--noUnusedLocals', '--allowJs'], options);
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
            var match = line.match(/^(.+)\((\d+),(\d+)\): error TS(\d+): '(\w+)'/);
            if (!match || match[4] !== '6133') continue;
            var file = match[1].replace(/\\/g, '/');
            if (file_name.slice(-file.length) !== file) continue;
            var line = Number(match[2]);
            var pos = Number(match[3]);
            var name = match[5];
            if (!Array.isArray(result[line])) {
                result[line] = [];
            }
            result[line].push({
                file: file,
                line: line,
                pos: pos,
                name: name,
            });
        }
        callback(null, result);
    });
};