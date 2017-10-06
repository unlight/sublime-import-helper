type NameOrNameArray = string | string[];

export const createname = 1;

export interface FullName {
	firstName: string;
	lastName: string;
}

export function createName(name: NameOrNameArray) {
    if (typeof name === "string") {
        return name;
    }
    else {
        return name.join(" ");
    }
}

var greetingMessage = `Greetings, ${ createName(["Sam", "Smith"]) }`;
alert(greetingMessage);