#import Console
#import Convert

#! get input as a number
int numinput

while true {
    numinput = Convert.toInt(Console.inp("> "))

    if numinput % 5 == 0 and numinput % 3 == 0 {
        Console.out("FizzBuzz")
    } else if numinput % 3 == 0 {
        Console.out("Fizz")
    } else if numinput % 5 == 0 {
        Console.out("Buzz")
    } else {
        Console.out(numinput)
    }
}