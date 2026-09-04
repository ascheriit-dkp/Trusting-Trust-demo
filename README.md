# Trusting Trust

Tiny implementation of Ken Thompson's [**Reflections on Trusting Trust**](https://doi.org/10.1145/358198.358210).

The idea is simple enough:

```text
clean source + infected compiler = infected binary
```

Slightly more annoying:

```text
clean compiler source + infected compiler = infected compiler
```

Put both together and you can end up with:

```text
clean program source
        +
clean compiler source
        +
previously infected compiler binary
        ↓
infected compiler
        ↓
infected program
```

So the program source is clean, the compiler source is clean, and the resulting binary is still infected.

Very reassuring.

## Files

`bootstrap.py` : trusted bootstrap used to build the first toy compiler.

`compiler.clean.src` : clean compiler source, explicitly marked as non-infected.

`compiler.evil.src` : used once to bootstrap the infected compiler.

`hello.src` : innocent target program. No payload here.

`demo.sh` : runs the entire chain inside `.demo/`.

## Run it

```bash
./demo.sh
```

The interesting part:

```text
compiler.evil.src
        ↓
compiler-infected
        |
        | compiles compiler.clean.src
        ↓
compiler-rebuilt
        |
        | compiles hello.src
        ↓
infected program
```

While:

```text
compiler.clean.src    clean
hello.src             clean
```

The infection survives through the compiler binary rather than the source being inspected.

Source review went great.

Anyway, have fun.
Maybe don't trust the compiler.
