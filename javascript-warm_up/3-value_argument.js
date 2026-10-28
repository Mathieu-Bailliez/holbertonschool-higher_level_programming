#!/usr/bin/node
const Args = process.argv
const nbArgs = process.argv.length - 2;

if (nbArgs === 0) {
  console.log('No argument');
} else {
    console.log(Args[2]);
}
