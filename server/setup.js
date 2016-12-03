const exec = require('child_process').exec;
exec('npm install --production', (error, stdout, stderr) => {
  if (error) {
    console.error(error);
    return;
  }
  console.log(stdout);
});