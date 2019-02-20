export class Greeter<T> {
    greeting: T;
    constructor(message: T) {
        this.greeting = message;
    }
    greet() {
        return this.greeting;
    }
}

export let greeter = new Greeter<string>("Hello, world");

let button = document.createElement('button');
button.textContent = "Say Hello";
button.onclick = function() {
    alert(greeter.greet());
}
// createName FullName Animal index1 index2 worker_threads fs readFileSync copyFileSync
document.body.appendChild(button);
// HTTP_STATUS_CONTINUE
function foo(res) {
	res.json(typeof HTTP2_HEADER_STATUS);
}

export const $goo = 1;
export const goo$ = 2;