# Trusting Trust

A tiny toy implementation of Ken Thompson's compiler trick.

Basically : the source code of both the target and the compiler can look completely clean while the resulting binaries are still infected.  
Which is a very comforting thing to remember.

This does not touch GCC, PAM, `/bin/login`, `/usr/bin/*`, or anything else you might regret breaking five minutes before a demo. No sudo, no root, no bricked Debian install. Tragically responsible stuff.

The idea is simple enough :

```text
clean source + infected compiler = infected binary
clean compiler source + infected compiler = infected compiler
```

Put both together and you end up with :

```text
compiler              infected
program               infected
```

While both :

```text
compiler.clean.src    clean
hello.src             clean
```

Which is fun.

<details>
<summary>Demo files</summary>

`bootstrap.py` : trusted bootstrap used to build the first toy compiler.  
`compiler.clean.src` : clean compiler source, explicitly marked as non-infected.  
`compiler.evil.src` : used once to bootstrap the infected compiler.  
`hello.src` : innocent target program. No payload here.  
`demo.sh` : runs the entire chain inside `.demo/`.

</details>

Computers are very obedient. The problem is occasionally figuring out who they were obedient to 👀.  

If your next thought is "okay, but where is the code for gcc?", congratulations on finding the exact thing this repo is not providing.  
If you've got enough time to build it, feel free to send it my way. I will, of course, review it very carefully under the extremely serious pretense of trusting-trust research purposes.

The full idea comes from Ken Thompson's 1984 paper, [**Reflections on Trusting Trust**](https://doi.org/10.1145/358198.358210). Give it a read, there is some genuinely fun stuff hiding in there.

Anyway, have fun. Trust nothing. Or maybe just keep trusting things the way you always have. That has historically gone great.

PS : I didn't invent shit, like always, so don't be surprised or whine about it.
