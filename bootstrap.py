#!/usr/bin/env python3
import json
import sys
from pathlib import Path

COMPILER_TEMPLATE = r'''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

INFECTED = @@INFECTED@@
SELF_TEMPLATE = @@TEMPLATE@@


def emit_program(src, dst):
    message = src["message"]
    code = f"""#!/usr/bin/env python3
print({message!r})
"""

    if INFECTED:
        code += 'print("[TRUSTING TRUST DEMO] payload injected by the compiler")\n'

    Path(dst).write_text(code)
    os.chmod(dst, 0o755)


def emit_compiler(src, dst):
    requested_infected = bool(src.get("infected", False))
    effective_infected = INFECTED or requested_infected

    inf_marker = "@@IN" + "FECTED@@"
    tpl_marker = "@@TE" + "MPLATE@@"

    code = (
        SELF_TEMPLATE
        .replace(inf_marker, repr(effective_infected))
        .replace(tpl_marker, repr(SELF_TEMPLATE))
    )

    Path(dst).write_text(code)
    os.chmod(dst, 0o755)


def main():
    if len(sys.argv) != 4 or sys.argv[1] != "-o":
        print(f"usage: {sys.argv[0]} -o OUTPUT SOURCE", file=sys.stderr)
        raise SystemExit(2)

    dst = sys.argv[2]
    src = json.loads(Path(sys.argv[3]).read_text())

    if src["type"] == "program":
        emit_program(src, dst)
    elif src["type"] == "compiler":
        emit_compiler(src, dst)
    else:
        raise SystemExit(f"unknown type: {src['type']!r}")


if __name__ == "__main__":
    main()
'''


def main():
    if len(sys.argv) != 4 or sys.argv[1] != "-o":
        print(f"usage: {sys.argv[0]} -o OUTPUT SOURCE", file=sys.stderr)
        raise SystemExit(2)

    dst = sys.argv[2]
    src = json.loads(Path(sys.argv[3]).read_text())

    if src["type"] != "compiler":
        raise SystemExit("bootstrap.py only builds the toy compiler")

    infected = bool(src.get("infected", False))
    inf_marker = "@@IN" + "FECTED@@"
    tpl_marker = "@@TE" + "MPLATE@@"

    code = (
        COMPILER_TEMPLATE
        .replace(inf_marker, repr(infected))
        .replace(tpl_marker, repr(COMPILER_TEMPLATE))
    )

    Path(dst).write_text(code)
    Path(dst).chmod(0o755)


if __name__ == "__main__":
    main()
