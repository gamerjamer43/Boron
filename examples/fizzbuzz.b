#! define fizzbuzz function
fn fizzbuzz(int numinput) -> str {
    if numinput % 5 == 0 and numinput % 3 == 0 {
        -> "FizzBuzz"
    } else if numinput % 3 == 0 {
        -> "Fizz"
    } else if numinput % 5 == 0 {
        -> "Buzz"
    } else {
        -> numinput
    }
}

#! while true
while true {
    int numinput = toInt(inp("> ")) #! take input, convert to int
    str fb = fizzbuzz(numinput) #! run it thru fizzbuzz function
    out(fb) #! print
}