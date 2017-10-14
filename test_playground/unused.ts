/// <reference types="node" />
import { Greeter as gr1 } from './greeter'; // Unused
import { FullName as f, createname as cr } from './createname'; // Partial
import {createname, FullName, createname as xx} from './createname';  // Unused all
import {Greeter} from './greeter'; // Used
import { Greeter as gr } from './greeter'; // Unused
import {greeter as lg} from './greeter'; // Used

console.log("Greeter", Greeter);
console.log("cr", cr);
console.log("lg", lg);