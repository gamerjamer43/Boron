#import Console
#import Convert

for (int i = 99; i > 2; i--) {
    Console.out(Convert.toStr(i) + " bottles of beer on the wall, " + Convert.toStr(i) + " bottles of beer!")
    Console.out("Take one down, pass it around, " + Convert.toStr(i-1) + " bottles of beer on the wall!")
}

Console.out("1 bottle of beer on the wall, 1 bottle of beer!")
Console.out("Take one down, pass it around, no more bottles of beer on the wall!")
Console.out("No more bottles of beer on the wall, no more bottles of beer!")
Console.out("Go to the store, buy some more, 99 more bottles of beer on the wall!")