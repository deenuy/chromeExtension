const child_process = require("child_process");
const fs = require("fs");
var fname = "./data/os_processes.txt";

const displayProcessBy = (pattern) => {
  let command = `ps ax -o comm | xargs -I % basename % | sort`;
  child_process.exec(command, (err, stdout, stdin) => {
    if (err) throw err;
    console.log("command executed successfully");
    console.log(stdout);
    try {
      fs.writeFileSync(fname, stdout);
    } catch (err) {
      console.error(err);
    }
  });
};

displayProcessBy("nodejs");
