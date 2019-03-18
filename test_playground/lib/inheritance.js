export class Animal {
    constructor(name) { }
    move(distanceInMeters = 0) {
        console.log(`${this.name} moved ${distanceInMeters}m.`);
    }
}

export class Snake extends Animal {
    constructor(name) { super(name); }
    move(distanceInMeters = 5) {
        console.log("Slithering...");
        super.move(distanceInMeters);
    }
}

export class Horse extends Animal {
    constructor(name) { super(name); }
    move(distanceInMeters = 45) {
        console.log("Galloping...");
        super.move(distanceInMeters);
    }
}

let sam = new Snake("Sammy the Python");
let tom = new Horse("Tommy the Palomino");

sam.move();
tom.move(34);