# Trusting Trust

A tiny toy implementation of Ken Thompson's **"Reflections on Trusting Trust"** compiler trick.

Basically: the source can look completely clean while the compiler built from it is still lying to you.
Which is a very comforting thing to remember about software supply chains.

This does **not** touch GCC, PAM, `/bin/login`, `/usr/bin/*`, or anything else you might regret breaking five minutes before a demo.
No `sudo`. No root. No bricked Debian install. Tragically responsible stuff.

## Just run the thing

```bash
chmod +x demo.sh
./demo.sh
```

You should end up seeing something along these lines:

```text
1/4 — boring, healthy compiler
Hello from the completely innocent program.

2/4 — same source, less trustworthy compiler
Hello from the completely innocent program.
[TRUSTING TRUST DEMO] payload injected by the compiler

Payload in hello.src? nope

3/4 — delete the obviously evil source
{
  "type": "compiler",
  "infected": false
}

4/4 — rebuild from the clean source using the infected compiler
Hello from the completely innocent program.
[TRUSTING TRUST DEMO] payload injected by the compiler
```

And there it is: clean compiler source, infected compiler binary.
Very normal. Nothing existential happening here.

## What is actually going on

The "language" is deliberately stupid. A source file is just JSON and the compiler emits tiny Python executables.
That keeps the interesting bit visible instead of burying it under an actual compiler toolchain.

There are two triggers:

1. An infected compiler sees a normal program and quietly appends a payload to the generated executable.
2. An infected compiler sees compiler source and forces the compiler it produces to stay infected, even when that source explicitly contains `"infected": false`.

So the fun little chain becomes:

```text
compiler.evil.src
        |
        | bootstrap.py
        v
compiler-infected
        |
        | compiles compiler.clean.src
        v
compiler-rebuilt
        |
        | compiles hello.src
        v
Hello from the completely innocent program.
[TRUSTING TRUST DEMO] payload injected by the compiler
```

The important part is this:

```text
compiler.clean.src  ->  "infected": false
compiler-rebuilt    ->  still infected
```

Because by that point the malicious state is carried by the **compiler doing the compilation**, not by the source you are staring at and feeling reassured by.

Auditing only the source is therefore not the same thing as establishing trust in the executable that came out the other end.
Annoying, but that's kind of the point.

## Files

- `bootstrap.py` — the deliberately trusted bootstrap used to create the first toy compiler.
- `compiler.clean.src` — compiler description saying it is clean.
- `compiler.evil.src` — compiler description used once to seed the infection.
- `hello.src` — innocent target program. It never contains the payload.
- `demo.sh` — runs the whole mess inside `.demo/` so the repository itself stays clean.

If you want to poke at it manually, the compiler interface is intentionally boring:

```bash
./bootstrap.py -o compiler-clean compiler.clean.src
./compiler-clean -o hello-clean hello.src
./hello-clean
```

Then seed the infected compiler:

```bash
./bootstrap.py -o compiler-infected compiler.evil.src
./compiler-infected -o hello-infected hello.src
./hello-infected
```

And finally rebuild from the clean compiler source with the infected compiler:

```bash
./compiler-infected -o compiler-rebuilt compiler.clean.src
./compiler-rebuilt -o hello-rebuilt hello.src
./hello-rebuilt
```

Yes, `compiler.clean.src` still says `false`.
Yes, `hello.src` still has no payload.
Yes, the generated program still prints it.

Computers are very obedient. The problem is occasionally figuring out who they were obedient to.

## Scope, before someone gets creative

This is a teaching toy, not a recipe for replacing a system compiler. It stays in the current directory, emits Python files, needs no privileges, and targets only its intentionally tiny JSON "language".

If your next thought is "okay but what if I do this to `/usr/bin/gcc`", congratulations on finding the exact thing this repo is avoiding.

The original idea comes from Ken Thompson's 1984 paper, **Reflections on Trusting Trust**.

Anyway, have fun. Trust nothing. Maybe trust `bootstrap.py`. Probably.
