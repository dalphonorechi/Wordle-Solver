### Wordle Solver

Consists of modlues that automate playing wordle.
Its built with selenium that used for web automation.

This together with [Datamuse Api](https://www.datamuse.com/api/), which has some very useful endpoints for requesting words, made it possible to easily automate solving wordle.

Although still buggy, the success of solving wordle is way higher than expected on the first try.


#### Cons

The biggest downside with this wordle solver is that if the HTML elements of worlde changes, the code has to be changed to match that since we read data from these elements.