#! get input as a number
int numinput

while true {
    numinput = toInt(inp("> "))

    if numinput % 5 == 0 and numinput % 3 == 0 {
        out("FizzBuzz")
    } else if numinput % 3 == 0 {
        out("Fizz")
    } else if numinput % 5 == 0 {
        out("Buzz")
    } else {
        out(numinput)
    }
}