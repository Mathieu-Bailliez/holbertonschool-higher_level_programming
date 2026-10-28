#!/usr/bin/node
const nbArgs = process.argv.length - 2;

if (nbArgs === 0) {
  console.log('No argument');
} else if (nbArgs === 1) {
  console.log('Argument found');
} else {
  console.log('Arguments found');
}
