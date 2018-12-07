/// <reference types="node" />
import { Greeter as gr1 } from './greeter'; // Unused
import { FullName as f, createname as cr } from './createname'; // Partial Used
import {createname, FullName, createname as xx} from './createname';  // Unused all
import {Greeter} from './greeter'; // Used
import { Greeter as gr } from './greeter'; // Unused
import {greeter as lg} from './greeter'; // Used
import * as someLib1 from 'prettier'; // Unused
import someLib2 from 'prettier'; // Unused
import $x from 'prettier'; // Unused
import { $x$ } from 'prettier'; // Unused
import {$x1, x as $xx, $x as $xxx, $a as x$} from 'd'; // Unused all

console.log("Greeter", Greeter);
console.log("cr", cr);
console.log("lg", lg);

console.log(typeof x2);